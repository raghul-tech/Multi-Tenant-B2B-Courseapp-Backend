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
        read_only_fields = ['id','created_at', 'updated_at']

class ModuleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'
    def validate(self, attrs):
        order = attrs.get('order', getattr(self.instance, 'order', None))
        course = attrs.get('course', getattr(self.instance, 'course', None))

        if order > 1: 
            if not Module.objects.filter(course = course,order = order-1).exists():
                raise serializers.ValidationError("You can add Module by order")

        return attrs

class ModuleEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
             'title',
             'description',
             "order"
        ]
    def validate(self, attrs):
        order = attrs.get('order', getattr(self.instance, 'order', None))
        course = attrs.get('course', getattr(self.instance, 'course', None))
        if order > 1: 
            if not Module.objects.filter(course = course,order = order-1).exists():
                raise serializers.ValidationError("You can edit Module by order")

        return attrs

class Module_Details_Serializer(serializers.ModelSerializer):
     class Meta: 
        model = Module
        fields = "__all__"
    
     submodules = SubModule_Details_Serializer(many=True,read_only=True)