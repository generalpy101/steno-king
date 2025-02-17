from django.urls import path
from .views import CourseListView, course_details

urlpatterns = [
    path("", CourseListView.as_view(), name="course-list"),
    path("<int:course_id>/", course_details, name="course-details"),
]
