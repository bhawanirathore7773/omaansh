from django.conf import settings
from django.db import models


class PasswordResetChallenge(models.Model):
    CHANNEL_CHOICES = (
        ("email", "Email"),
        ("phone", "Phone"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_challenges",
    )
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    target = models.CharField(max_length=254)
    otp_hash = models.CharField(max_length=255, blank=True)
    provider_sid = models.CharField(max_length=80, blank=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    verified_at = models.DateTimeField(null=True, blank=True)
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["target", "created_at"]),
        ]

    def __str__(self):
        return f"{self.channel} recovery for {self.user.get_username()}"
