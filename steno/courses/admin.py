from django.contrib import admin

from .models import Course, CourseBundle, CourseTopic, CoursePurchase


# Register your models here.
admin.site.register(Course)
admin.site.register(CourseBundle)
admin.site.register(CourseTopic)
admin.site.register(CoursePurchase)
