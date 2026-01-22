from rest_framework import serializers
from .models import UserCourseProgress

class courseprogress_view_serializers(serializers.ModelSerializer):
    class Meta:
        model = UserCourseProgress
        fields = '__all__'
        read_only_fields = [field.name for field in model._meta.fields]

class courseprogress_create_serializers(serializers.ModelSerializer):
    class Meta:
        model = UserCourseProgress
        fields = [
            "user",
            "tenant",
            "course",
            "course_progress",
            "course_completed",
        ]
        read_only_fields = ["tenant"]


    def validate(self, attrs):
        user = self.context['request'].user
        if attrs['user'].tenant != user.tenant or attrs['course'].tenant != user.tenant:
            return serializers.ValidationError("Tenant id is different ")
        if UserCourseProgress.objects.filter(
            user = attrs['user'],
            course = attrs['course']
        ).exists():
            return serializers.ValidationError("Course progress already exists ")

        return super().validate(attrs)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['tenant'] = user.tenant
        return super().create(validated_data)
    
