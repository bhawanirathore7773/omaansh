from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import redirect, render
from django.core.cache import cache
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .models import PasswordResetChallenge
from .services import (
    MAX_ATTEMPTS,
    can_request_reset,
    create_email_challenge,
    create_phone_challenge,
    email_otp_is_valid,
    find_admin_by_email,
    find_admin_by_phone,
    generate_email_otp,
    normalize_phone,
    send_email_otp,
    send_phone_otp,
    verify_phone_otp,
)


def _clear_reset_session(request):
    for key in (
        "reset_challenge_id",
        "reset_identifier",
        "reset_verified",
    ):
        request.session.pop(key, None)


@require_http_methods(["GET", "POST"])
def admin_forgot_password(request):
    step = "request"
    challenge = None

    if request.GET.get("restart") == "1":
        _clear_reset_session(request)

    challenge_id = request.session.get("reset_challenge_id")
    if challenge_id:
        challenge = PasswordResetChallenge.objects.filter(pk=challenge_id).first()
        if challenge and challenge.used_at:
            _clear_reset_session(request)
            challenge = None
        elif challenge and challenge.expires_at <= timezone.now():
            _clear_reset_session(request)
            challenge = None
        elif challenge:
            step = "verify" if not request.session.get("reset_verified") else "reset"

    if request.method == "POST":
        action = request.POST.get("action", "").strip()

        if action == "send":
            method = request.POST.get("method", "email")
            identifier = request.POST.get("identifier", "").strip()

            if method == "phone":
                target = normalize_phone(identifier)
                user = find_admin_by_phone(identifier)
            else:
                target = identifier.lower()
                user = find_admin_by_email(identifier)

            allowed, wait_message = can_request_reset(target)
            if not target or not user:
                # Keep account existence private.
                messages.success(
                    request,
                    "If the account is registered, a verification code will be sent shortly.",
                )
                return render(request, "admin/forgot_password.html", {"step": "request"})

            if not allowed:
                messages.warning(request, wait_message)
                return render(request, "admin/forgot_password.html", {"step": "request"})

            PasswordResetChallenge.objects.filter(
                user=user,
                used_at__isnull=True,
                verified_at__isnull=True,
            ).update(used_at=timezone.now())

            if method == "phone":
                challenge = create_phone_challenge(user, target)
                try:
                    sid = send_phone_otp(challenge)
                    challenge.provider_sid = sid
                    challenge.save(update_fields=["provider_sid"])
                except Exception:
                    challenge.delete()
                    messages.error(
                        request,
                        "SMS verification is temporarily unavailable. Please use email recovery.",
                    )
                    return render(request, "admin/forgot_password.html", {"step": "request"})
            else:
                otp = generate_email_otp()
                challenge = create_email_challenge(user, target, otp)
                try:
                    send_email_otp(challenge)
                except Exception:
                    challenge.delete()
                    messages.error(
                        request,
                        "We could not send the email right now. Please try again later.",
                    )
                    return render(request, "admin/forgot_password.html", {"step": "request"})

            request.session["reset_challenge_id"] = challenge.id
            request.session["reset_identifier"] = target
            request.session["reset_verified"] = False
            request.session.modified = True
            messages.success(
                request,
                "Verification code sent. It expires in 10 minutes.",
            )
            return redirect("admin_forgot_password")

        if action == "verify":
            challenge_id = request.session.get("reset_challenge_id")
            challenge = PasswordResetChallenge.objects.filter(pk=challenge_id).first()
            if not challenge or challenge.expires_at <= timezone.now() or challenge.used_at:
                _clear_reset_session(request)
                messages.error(request, "This verification session has expired. Start again.")
                return redirect("admin_forgot_password")

            code = request.POST.get("otp", "").strip()
            if len(code) != 6 or not code.isdigit():
                messages.error(request, "Enter the 6-digit verification code.")
                return render(request, "admin/forgot_password.html", {"step": "verify"})

            if challenge.attempts >= MAX_ATTEMPTS:
                _clear_reset_session(request)
                messages.error(request, "Too many incorrect attempts. Start a new recovery.")
                return redirect("admin_forgot_password")

            challenge.attempts += 1
            challenge.save(update_fields=["attempts"])

            if challenge.channel == "phone":
                valid = verify_phone_otp(challenge, code)
            else:
                valid = email_otp_is_valid(challenge, code)

            if not valid:
                remaining = MAX_ATTEMPTS - challenge.attempts
                messages.error(request, f"Invalid code. {remaining} attempts remaining.")
                return render(request, "admin/forgot_password.html", {"step": "verify"})

            challenge.verified_at = timezone.now()
            challenge.save(update_fields=["verified_at"])
            request.session["reset_verified"] = True
            request.session.modified = True
            messages.success(request, "Identity verified. Set your new password.")
            return redirect("admin_forgot_password")

        if action == "reset":
            challenge_id = request.session.get("reset_challenge_id")
            challenge = PasswordResetChallenge.objects.select_related("user").filter(pk=challenge_id).first()
            if not challenge or not request.session.get("reset_verified"):
                _clear_reset_session(request)
                return redirect("admin_forgot_password")

            if challenge.expires_at <= timezone.now() or not challenge.verified_at:
                _clear_reset_session(request)
                messages.error(request, "This verification session has expired. Start again.")
                return redirect("admin_forgot_password")

            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")

            if len(password1) < 12:
                messages.error(request, "Use a password of at least 12 characters.")
                return render(request, "admin/forgot_password.html", {"step": "reset"})
            if password1 != password2:
                messages.error(request, "The passwords do not match.")
                return render(request, "admin/forgot_password.html", {"step": "reset"})

            challenge.user.set_password(password1)
            challenge.user.save(update_fields=["password"])
            challenge.used_at = timezone.now()
            challenge.save(update_fields=["used_at"])
            _clear_reset_session(request)
            request.session.cycle_key()
            messages.success(request, "Password updated successfully. You can now sign in.")
            return redirect("admin:login")

    return render(request, "admin/forgot_password.html", {"step": step, "challenge": challenge})


@require_http_methods(["GET", "POST"])
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin:index")

    if request.method == "POST":
        identifier = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        remember = request.POST.get("remember") == "on"

        User = get_user_model()
        user = User.objects.filter(email__iexact=identifier, is_active=True).first()
        username = user.username if user else identifier
        rate_key = f"hoovale-admin-login:{request.META.get('REMOTE_ADDR', 'unknown')}:{username.lower()}"
        attempts = cache.get(rate_key, 0)
        if attempts >= 10:
            messages.error(request, "Too many sign-in attempts. Please wait 15 minutes and try again.")
            return render(request, "admin/login.html", {"next": request.POST.get("next", "")})

        authenticated = authenticate(request, username=username, password=password)

        if authenticated and authenticated.is_staff:
            login(request, authenticated)
            request.session.set_expiry(60 * 60 * 24 * 30 if remember else 0)
            next_url = request.POST.get("next") or request.GET.get("next") or reverse("admin:index")
            if not url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                next_url = reverse("admin:index")
            return redirect(next_url)

        cache.set(rate_key, attempts + 1, 60 * 15)
        messages.error(request, "The email/username or password is incorrect.")

    return render(request, "admin/login.html", {
        "next": request.GET.get("next", ""),
    })
