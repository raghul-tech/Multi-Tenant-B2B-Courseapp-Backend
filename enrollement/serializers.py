from rest_framework import serializers
from .models import Enrollement

class EnrollementSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    class Meta:
        model = Enrollement
        fields = '__all__'
        