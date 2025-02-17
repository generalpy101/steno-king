from django.db import models
from django.conf import settings

from ckeditor.fields import RichTextField
from datetime import datetime
from courses.models import Course

# # ------------------------------------------
# # Test Series (Grouping of Tests)
# # ------------------------------------------
# class TestSeries(models.Model):
#     """Groups multiple tests together (e.g., SSC CGL, Banking Exams)."""

#     name = models.CharField(max_length=255, unique=True)  # Test series name
#     description = models.TextField(blank=True, null=True)  # Optional description
#     created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

#     def __str__(self):
#         return self.name


# # ------------------------------------------
# # Test Model (Typing Test, Steno Test, etc.)
# # ------------------------------------------
# class Test(models.Model):
#     """Represents a test (typing or steno)."""

#     TEST_TYPE_CHOICES = [
#         ('typing', 'Typing Test'),
#         ('steno', 'Steno Test'),
#     ]

#     name = models.CharField(max_length=255)  # Test name
#     description = models.TextField(blank=True, null=True)  # Optional description
#     test_series = models.ForeignKey(TestSeries, on_delete=models.CASCADE, related_name="tests", blank=True, null=True)  # Grouping (optional)
#     test_type = models.CharField(max_length=10, choices=TEST_TYPE_CHOICES, default='typing')  # Type of test
#     content = RichTextField()  # Text to type (for typing tests), or transcript (for steno tests)
#     audio_file = models.FileField(upload_to="steno_audio/", blank=True, null=True)  # For steno tests
#     is_timed = models.BooleanField(default=True)  # Timed test? If yes, time_limit is requiredq
#     time_limit = models.IntegerField(blank=True, null=True)  # Time limit in seconds
#     is_backspace_allowed = models.BooleanField(default=True)  # Allow backspace?
#     is_case_sensitive = models.BooleanField(default=False)  # Case sensitive?
#     max_score = models.IntegerField(default=100)  # Maximum score

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.name} ({self.get_test_type_display()})"


# # ------------------------------------------
# # User Test Attempts
# # ------------------------------------------
# class TestAttempt(models.Model):
#     """Stores user attempts for a test."""

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="test_attempts")
#     test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="attempts")
#     score = models.FloatField()  # Score obtained
#     time_taken = models.IntegerField(help_text="Time taken in seconds")  # Time spent
#     submitted_at = models.DateTimeField(auto_now_add=True)  # Timestamp
#     user_input = models.TextField()  # User's typed text (for typing tests), or steno transcript (for steno tests)
#     extra_info = models.JSONField(blank=True, null=True)  # Extra info (e.g., errors, accuracy, etc.). JSON for extensibility

#     def __str__(self):
#         return f"{self.user.username} - {self.test.name} ({self.score})"


class Test(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="tests", null=True, blank=True
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    test_type = models.CharField(
        max_length=10, choices=[("typing", "Typing"), ("steno", "Steno")]
    )
    is_steno = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_backspace_allowed = models.BooleanField(default=True)
    is_timed = models.BooleanField(default=True)
    time_limit = models.IntegerField(null=True, blank=True)  # In seconds
    is_case_sensitive = models.BooleanField(default=False)
    content = RichTextField(blank=True, null=True)
    audio_file = models.FileField(
        upload_to="audio_tests/", null=True, blank=True
    )  # For steno

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TestAttempt(models.Model):
    """Stores user attempts for a test."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="test_attempts"
    )
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="attempts")
    score = models.FloatField()  # Score obtained
    time_taken = models.IntegerField(help_text="Time taken in seconds")  # Time spent
    submitted_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    user_input = (
        models.TextField()
    )  # User's typed text (for typing tests), or steno transcript (for steno tests)
    extra_info = models.JSONField(
        blank=True, null=True
    )  # Extra info (e.g., errors, accuracy, etc.). JSON for extensibility

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.test.name} ({self.score})"


# class StudyMaterial(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="study_materials")
#     title = models.CharField(max_length=255)
#     file = models.FileField(upload_to="study_materials/")
#     description = models.TextField(blank=True)
