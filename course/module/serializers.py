from rest_framework import serializers
from course.models import Module
from course.submodule.serializers import SubModule_Details_Serializer
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
            'id',
            'course',
            'title',
            'description',
            'order',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class Module_Details_Serializer(serializers.ModelSerializer):
     class Meta: 
        model = Module
        fields = "__all__"
    
     submodules = SubModule_Details_Serializer(many=True,read_only=True)