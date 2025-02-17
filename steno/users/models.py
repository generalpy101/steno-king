from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser."""

    email = models.EmailField(unique=True)  # Ensure unique emails for login
    phone_number = models.CharField(
        max_length=15, blank=True, null=True
    )  # Optional phone number
    is_subscribed = models.BooleanField(
        default=False
    )  # Tracks active subscription status
    subscription_expires_at = models.DateTimeField(
        null=True, blank=True
    )  # Expiry date for subscription

    def __str__(self):
        return self.username
