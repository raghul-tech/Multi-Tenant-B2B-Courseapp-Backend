from rest_framework import serializers
from  .models import Course_db
from .module.serializers import Module_Details_Serializer

class CourseSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Course_db
        fields = [
            'id',
            'title',
            'description',
            'skills',
            'created_at',
            'updated_at',
            'course_type',
            'price',
            'status'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class Course_Details_Serializer(serializers.ModelSerializer):
     class Meta: 
        model = Course_db
        fields = "__all__"

     modules = Module_Details_Serializer(many=True,read_only=True)

