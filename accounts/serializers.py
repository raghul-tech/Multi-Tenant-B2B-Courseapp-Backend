from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login
#from validate_email_address import validate_email
from django.core.validators import validate_email
from django.core.exceptions import ValidationError



            
class EmailTokenSerializer(TokenObtainPairSerializer): 
    username_field =  User.USERNAME_FIELD
    def validate(self, attrs):  
        try:
            validate_email(attrs.get(self.username_field))
        except Exception:
             raise serializers.ValidationError({"email is not valid"})
        data = super().validate(attrs)
        update_last_login(None, self.user)
        return data
    
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
           

          
class UserAdminSerializerCreate(serializers.ModelSerializer):
      password = serializers.CharField(write_only=True)
      class Meta:
            model = User
            fields = ['id', 'email', 'password', 'tenant', 'is_active', 'is_staff']    
            read_only_fields = ['id']

      def validate(self, attrs):
            request = self.context['request']
            user = request.user
            tenant = attrs.get('tenant')
            email = attrs.get('email')
            try:
              validate_email(email)
            except ValidationError:
                  raise serializers.ValidationError("Email is not valid")
            if User.objects.filter(email = email).exists():
                  raise serializers.ValidationError("Email is already exists")
            
            if user.role == User.SUPER_ADMIN and not tenant:
                  raise serializers.ValidationError("super admin should give tenant")
            if user.role == User.TENANT_ADMIN and tenant:
                  raise serializers.ValidationError("tenant admin cannot give tenant")
            if tenant and not tenant.is_active:
                  raise serializers.ValidationError("tenant is not active")
            
            return attrs
      
      def create(self, validated_data):
            password = validated_data.pop('password')
            request = self.context['request']
            user = request.user
            if user.role == User.TENANT_ADMIN:
                  validated_data['tenant'] = user.tenant
            validated_data['role'] = User.TENANT_ADMIN
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            return user
      

class UserEditSerializer(serializers.ModelSerializer):
      password = serializers.CharField(write_only=True,required=False)
      class Meta:
            model = User
            fields = [
                  'email',
                  'password',
                  "is_active",
                  "is_staff",
            ]

      def validate(self, attrs):
            email = attrs.get('email')
            if email:
                try:
                    validate_email(email)
                except ValidationError:
                        raise serializers.ValidationError("Email is not valid")
            if User.objects.filter(email = email).exists():
                  raise serializers.ValidationError("Email is already exists")
                
            return attrs
      
      def update(self, instance, validated_data):
            password = validated_data.pop('password',None)
            for attrs,value in validated_data.items():
                  setattr(instance,attrs,value)
            if password:
                  instance.set_password(password)
            instance.save()
            return instance
     