from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    """Customize the User model display in Django Admin."""

    model = User
    list_display = (
        "username",
        "email",
        "phone_number",
        "is_subscribed",
        "subscription_expires_at",
        "is_active",
        "is_staff",
    )
    fieldsets = UserAdmin.fieldsets + (
        ("Subscription Info", {"fields": ("is_subscribed", "subscription_expires_at")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Subscription Info", {"fields": ("is_subscribed", "subscription_expires_at")}),
    )


admin.site.register(User, CustomUserAdmin)
