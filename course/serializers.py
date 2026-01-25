from rest_framework import serializers
from  .models import Course_db
from .module.serializers import Module_Details_Serializer
from skills.models import Skills,CourseSkill

class CourseSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Course_db
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'updated_at',
            'course_type',
            'price',
            'status'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class AddSkillSerializer(serializers.Serializer):
    name = serializers.CharField()
    weight = serializers.IntegerField(min_value=1,max_value=100)

class CourseCreateSerializer(serializers.ModelSerializer):
    skills = AddSkillSerializer(many= True,write_only = True)
    class Meta:
        model = Course_db
        fields =[
            'title',
            'description',
             'course_type',
             'price',
            'status',
            'skills'
        ]

    def validate(self, attrs):
        title = attrs.get('title')
        tenant = self.context['request'].user.tenant
        if Course_db.objects.filter(title = title,tenant = tenant).exist():
            raise serializers.ValidationError("Course already Exists")
        return super().validate(attrs)

    def create(self, validated_data):
        skills = validated_data.pop('skills')
        user = self.context['request'].user
        tenant = user.tenant
        course = Course_db.objects.create(
            tenant = tenant,
            created_by = user,
            **validated_data)

        for skill_name in skills:
            skill,_ = Skills.objects.get_or_create(
                name = skill_name['name'],
                 tenant = tenant
            )
            CourseSkill.objects.get_or_create(
                tenant= tenant,
                course = course,
                skills = skill,
                course_weight = skill_name['weight']
            )


        return course


class Course_Details_Serializer(serializers.ModelSerializer):
     class Meta: 
        model = Course_db
        fields = "__all__"

     modules = Module_Details_Serializer(many=True,read_only=True)

