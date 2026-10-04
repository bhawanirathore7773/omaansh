from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PasswordResetChallenge",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "channel",
                    models.CharField(
                        choices=[("email", "Email"), ("phone", "Phone")],
                        max_length=10,
                    ),
                ),
                ("target", models.CharField(max_length=254)),
                ("otp_hash", models.CharField(blank=True, max_length=255)),
                ("provider_sid", models.CharField(blank=True, max_length=80)),
                ("expires_at", models.DateTimeField()),
                ("attempts", models.PositiveSmallIntegerField(default=0)),
                ("verified_at", models.DateTimeField(blank=True, null=True)),
                ("used_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="password_reset_challenges",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="passwordresetchallenge",
            index=models.Index(
                fields=["user", "created_at"],
                name="accounts_pa_user_id_2d4f6c_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="passwordresetchallenge",
            index=models.Index(
                fields=["target", "created_at"],
                name="accounts_pa_target_4d3b0a_idx",
            ),
        ),
    ]
