import logging
import secrets
import hashlib
from datetime import timedelta

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.template.loader import render_to_string
from django.utils import timezone

from .models import PasswordResetChallenge


logger = logging.getLogger(__name__)

OTP_TTL_MINUTES = 10
MAX_ATTEMPTS = 5
RESEND_COOLDOWN_SECONDS = 60
MAX_REQUESTS_PER_15_MINUTES = 5


def normalize_phone(value: str) -> str:
    digits = "".join(ch for ch in (value or "") if ch.isdigit())
    if digits.startswith("91") and len(digits) == 12:
        return f"+{digits}"
    if len(digits) == 10:
        return f"+91{digits}"
    if (value or "").strip().startswith("+") and len(digits) >= 10:
        return f"+{digits}"
    return ""


def target_digest(value: str) -> str:
    return hashlib.sha256(value.strip().lower().encode("utf-8")).hexdigest()


def find_admin_by_email(email: str):
    User = get_user_model()
    return User.objects.filter(
        email__iexact=email.strip(),
        is_active=True,
        is_staff=True,
    ).first()


def find_admin_by_phone(phone: str):
    normalized = normalize_phone(phone)
    configured = normalize_phone(getattr(settings, "ADMIN_RESET_PHONE", ""))
    if not normalized or not configured or normalized != configured:
        return None

    User = get_user_model()
    username = getattr(settings, "ADMIN_RESET_USERNAME", "admin")
    return User.objects.filter(
        username=username,
        is_active=True,
        is_staff=True,
    ).first()


def generate_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def generate_email_otp() -> str:
    return generate_otp()


def can_request_reset(target: str) -> tuple[bool, str]:
    target = target.strip().lower()
    if not target:
        return False, "Invalid recovery target."

    now = timezone.now()
    recent = PasswordResetChallenge.objects.filter(
        target=target,
        created_at__gte=now - timedelta(minutes=15),
    ).count()
    if recent >= MAX_REQUESTS_PER_15_MINUTES:
        return False, "Too many requests. Please try again later."

    latest = PasswordResetChallenge.objects.filter(target=target).first()
    if latest and (now - latest.created_at).total_seconds() < RESEND_COOLDOWN_SECONDS:
        return False, "Please wait a minute before requesting another code."

    return True, ""


def _render_otp_email(otp: str) -> tuple[str, str, str]:
    subject = "Your HOOVALE Admin password reset OTP"
    context = {
        "otp": otp,
        "expires_minutes": OTP_TTL_MINUTES,
        "year": timezone.now().year,
    }
    html = render_to_string("accounts/email/password_reset_otp.html", context)
    text = (
        "HOOVALE Admin password reset\n\n"
        f"Your one-time verification code is {otp}.\n"
        f"This code expires in {OTP_TTL_MINUTES} minutes.\n\n"
        "If you did not request this, you can safely ignore this email."
    )
    return subject, text, html


def send_email_otp(challenge: PasswordResetChallenge, otp: str) -> str:
    provider = getattr(settings, "OTP_EMAIL_PROVIDER", "brevo").strip().lower()
    subject, text, html = _render_otp_email(otp)

    if provider == "console":
        logger.warning(
            "HOOVALE TEST OTP [email] target=%s otp=%s expires=%s minutes",
            challenge.target,
            otp,
            OTP_TTL_MINUTES,
        )
        return "console"

    if provider != "brevo":
        raise RuntimeError("Unsupported email OTP provider.")

    api_key = getattr(settings, "BREVO_API_KEY", "")
    sender_email = getattr(settings, "BREVO_SENDER_EMAIL", "")
    sender_name = getattr(settings, "BREVO_SENDER_NAME", "HOOVALE")
    if not api_key or not sender_email:
        raise RuntimeError("Brevo email OTP is not configured.")

    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json",
        },
        json={
            "sender": {"name": sender_name, "email": sender_email},
            "to": [{"email": challenge.target}],
            "subject": subject,
            "htmlContent": html,
            "textContent": text,
            "tags": ["hoovale-admin-password-reset"],
        },
        timeout=12,
    )
    if response.status_code >= 400:
        logger.error("Brevo OTP send failed with HTTP %s", response.status_code)
        raise RuntimeError("Email OTP could not be sent.")

    return response.json().get("messageId", "")


def send_phone_otp(challenge: PasswordResetChallenge) -> str:
    provider = getattr(settings, "OTP_SMS_PROVIDER", "twilio").strip().lower()

    if provider == "console":
        otp = generate_otp()
        challenge.otp_hash = make_password(otp)
        challenge.save(update_fields=["otp_hash"])
        logger.warning(
            "HOOVALE TEST OTP [phone] target=%s otp=%s expires=%s minutes",
            challenge.target,
            otp,
            OTP_TTL_MINUTES,
        )
        return "console"

    if provider != "twilio":
        raise RuntimeError("Unsupported SMS OTP provider.")

    account_sid = getattr(settings, "TWILIO_ACCOUNT_SID", "")
    auth_token = getattr(settings, "TWILIO_AUTH_TOKEN", "")
    service_sid = getattr(settings, "TWILIO_VERIFY_SERVICE_SID", "")

    if not all((account_sid, auth_token, service_sid)):
        raise RuntimeError("Twilio phone OTP is not configured.")

    response = requests.post(
        f"https://verify.twilio.com/v2/Services/{service_sid}/Verifications",
        auth=(account_sid, auth_token),
        data={"To": challenge.target, "Channel": "sms"},
        timeout=12,
    )
    if response.status_code >= 400:
        logger.error("Twilio OTP send failed with HTTP %s", response.status_code)
        raise RuntimeError("SMS OTP could not be sent.")

    payload = response.json()
    return payload.get("sid", "")


def verify_phone_otp(challenge: PasswordResetChallenge, code: str) -> bool:
    provider = getattr(settings, "OTP_SMS_PROVIDER", "twilio").strip().lower()

    if provider == "console":
        return email_otp_is_valid(challenge, code)

    if provider != "twilio":
        return False

    account_sid = getattr(settings, "TWILIO_ACCOUNT_SID", "")
    auth_token = getattr(settings, "TWILIO_AUTH_TOKEN", "")
    service_sid = getattr(settings, "TWILIO_VERIFY_SERVICE_SID", "")

    if not all((account_sid, auth_token, service_sid)):
        return False

    response = requests.post(
        f"https://verify.twilio.com/v2/Services/{service_sid}/VerificationCheck",
        auth=(account_sid, auth_token),
        data={"To": challenge.target, "Code": code},
        timeout=12,
    )
    if response.status_code >= 400:
        return False
    return response.json().get("status") == "approved"


def create_email_challenge(user, email: str, otp: str) -> PasswordResetChallenge:
    return PasswordResetChallenge.objects.create(
        user=user,
        channel="email",
        target=email.strip().lower(),
        otp_hash=make_password(otp),
        expires_at=timezone.now() + timedelta(minutes=OTP_TTL_MINUTES),
    )


def create_phone_challenge(user, phone: str) -> PasswordResetChallenge:
    return PasswordResetChallenge.objects.create(
        user=user,
        channel="phone",
        target=normalize_phone(phone),
        expires_at=timezone.now() + timedelta(minutes=OTP_TTL_MINUTES),
    )


def email_otp_is_valid(challenge: PasswordResetChallenge, code: str) -> bool:
    return bool(challenge.otp_hash) and check_password(code, challenge.otp_hash)
