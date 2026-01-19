from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login


class UserSerializer(serializers.ModelSerializer):  
    class Meta:
        password = serializers.CharField(write_only=True)
        model = User
        fields = ['id', 'email', 'password', 'role', 'tenant', 'is_active', 'is_staff']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self,instance,validated_data):
                password = validated_data.pop('password')
                for attr ,value in validated_data.items():
                     setattr(instance,attr,value)

                if password:
                     instance.set_password(password)
                
                instance.save()
                return instance

                






  

class EmailTokenSerializer(TokenObtainPairSerializer): 
    username_field =  User.USERNAME_FIELD
    def validate(self, attrs):  
        data = super().validate(attrs)
        update_last_login(None, self.user)
        return data