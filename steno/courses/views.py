from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Course, CourseTopic, CoursePurchase
from .serializers import CourseSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from test_series.models import Test


class CourseListView(generics.ListAPIView):
    """
    API to list courses with optional filters:
    - ?topic=<topic_name> → Filter by topic
    - ?enrolled=true → Show only enrolled courses
    - Both can be combined
    """

    serializer_class = CourseSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # Auth required for enrolled filter

    def get_queryset(self):
        queryset = Course.objects.all()

        # Filter by topic if provided
        topic_name = self.request.query_params.get("topic")
        if topic_name:
            topic = get_object_or_404(CourseTopic, name__iexact=topic_name)
            queryset = queryset.filter(topic=topic)

        # Filter by enrolled courses if 'enrolled=true' is passed
        enrolled = self.request.query_params.get("enrolled")
        if enrolled and enrolled.lower() == "true":
            if self.request.user.is_authenticated:
                purchased_courses = CoursePurchase.objects.filter(
                    user=self.request.user
                ).values_list("course_id", flat=True)
                queryset = queryset.filter(id__in=purchased_courses)
            else:
                return Course.objects.none()  # Return empty if not logged in

        return queryset


@login_required
def course_details(request, course_id):
    user_id = request.user.id
    course = get_object_or_404(Course, id=course_id)
    # Check if user has purchased this course
    is_purchased = CoursePurchase.objects.filter(
        user_id=user_id, course_id=course_id
    ).exists()

    # Get all contents (Tests, study material, etc.) for this course
    tests = Test.objects.filter(course=course).all()

    # Group contents by type for easy rendering
    course_contents = {
        "tests": tests,
    }

    return render(
        request,
        "course_details.html",
        {
            "course": course,
            "is_purchased": is_purchased,
            "course_contents": course_contents,
        },
    )
