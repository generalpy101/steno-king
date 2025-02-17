from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    topic = serializers.StringRelatedField()  # Returns topic name instead of ID

    class Meta:
        model = Course
        fields = "__all__"
