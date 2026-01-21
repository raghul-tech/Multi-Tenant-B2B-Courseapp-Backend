from rest_framework import serializers
from skills.models import CourseSkill

class CourseSkill_View_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSkill
        fields = [
            "id",
            "course",
            "skills",
            "tenant",
            "course_weight",
            "created_at"
        ]
        read_only_fields = fields

class CourseSkill_Create_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSkill
        fields =[
            "skills",
            "course",
            "course_weight",
        ]

    def validate(self, attrs):
        user = self.context['request'].user
        if attrs['skills'].tenant != user.tenant:
            raise serializers.ValidationError("this skill was not found")
        if attrs['course'].tenant != user.tenant:
            raise serializers.ValidationError("course was not found ")
        
        if CourseSkill.objects.filter(
                skills = attrs['skills'],
                course = attrs['course']
            ).exists():
            raise serializers.ValidationError("Course is already there ")

        return super().validate(attrs)
    
    def create(self,validated_data):
        user = self.context['request'].user
        validated_data['tenant'] = user.tenant
        return super().create(validated_data)
        
class CourseSkill_Edit_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSkill
        fields =[
            "course_weight"
        ]
    
  
    
    