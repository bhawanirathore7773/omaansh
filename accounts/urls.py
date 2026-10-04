from django.urls import path
from .views import admin_forgot_password

urlpatterns = [
    path("admin/forgot-password/", admin_forgot_password, name="admin_forgot_password"),
]
