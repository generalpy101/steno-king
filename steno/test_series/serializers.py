from rest_framework import serializers
from .models import Test


class TestSerializer(serializers.ModelSerializer):
    topic = serializers.StringRelatedField()  # Returns topic name instead of ID

    class Meta:
        model = Test
        fields = "__all__"
