from rest_framework import serializers
from accounts.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UserSerializerView(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ['id', 'email', 'password', 'role', 'tenant', 'is_active', 'is_staff']

class UserSerializerCreate(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
         model = User
         fields = ['id', 'email', 'password', 'is_active', 'is_staff']
        
    def validate(self, attrs):
         email = attrs.get('email')
         try:
              validate_email(email)
         except ValidationError:
              raise serializers.ValidationError("Email is not valid")
         
         if User.objects.filter(email = email).exists():
              raise serializers.ValidationError("Email is already exists")
            
         return attrs
    
    def create(self, validated_data):
         password = validated_data.pop('password')
         validated_data['role'] = User.TENANT_USER
         user = User(**validated_data)
         user.set_password(password)
         user.save()
         return user
    
class UserSerializerEdit(serializers.ModelSerializer):
      password = serializers.CharField(write_only=True,required=False)
      class Meta:
         model = User
         fields = ['id', 'email', 'password', 'is_active', 'is_staff']

      def validate(self, attrs):
         email = attrs.get('email')
         try:
              validate_email(email)
         except ValidationError:
              raise serializers.ValidationError("Email is not valid")
           
         return attrs
      
      def update(self, instance, validated_data):
           password = validated_data.pop('password',None)
           for attrs,value in validated_data.items():
                setattr(instance,attrs,value)
           if password:
                instance.set_password(password)
           instance.save()
           return instance