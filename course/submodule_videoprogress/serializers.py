from rest_framework import serializers
from course.models import VideoProgress

class VideoProgress_Serializer(serializers.ModelSerializer):
    class Meta:
        model = VideoProgress
        fields= "__all__"
