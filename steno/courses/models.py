from django.db import models
from django.conf import settings


# Create your models here.
class CourseTopic(models.Model):
    name = models.CharField(
        max_length=255, unique=True
    )  # Typing, Steno, Study Material, etc.
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Change topic to lowercase always
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(CourseTopic, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    topic = models.ForeignKey(
        CourseTopic, on_delete=models.CASCADE, related_name="courses"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  # Optional if pricing varies later
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CourseBundle(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    courses = models.ManyToManyField(Course, related_name="bundles")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CoursePurchase(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="purchases"
    )
    course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="purchases",
    )
    bundle = models.ForeignKey(
        CourseBundle, null=True, blank=True, on_delete=models.CASCADE
    )
    purchase_date = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
