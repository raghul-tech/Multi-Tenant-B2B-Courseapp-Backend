from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializerView, EmailTokenSerializer,UserSerializerCreate,UserAdminSerializerCreate,UserEditSerializer
from rest_framework.permissions import IsAuthenticated
from core.permission import IsSuperAdmin,IsTenantAdmin,IsSuperAdminOrTenantAdmin,IsTenantAdminOrUser
from rest_framework_simplejwt.views import TokenObtainPairView 
from validate_email_address import validate_email
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView,GenericAPIView,get_object_or_404
from tenant.models import Tenant
 

# Create your views here.
class account_create_superuser(APIView):
      permission_classes = [IsAuthenticated,IsSuperAdmin]
      def post(self,request):
            email = request.data.get("email")
            passwd = request.data.get("password")

            if not validate_email(email):
                  return Response({"email is not valid"},status=403)
            if not email or not passwd:
                  return Response({"details":"email and password is required"},status=403)
            if User.objects.filter(email = email).exists():
                  return Response({"Email already exist"},status=403)
            super_user =  User.objects.create_superuser (
                  email = email,
                  password = passwd
             )

            serializer = UserSerializerView(super_user)
            return Response(serializer.data,status=200)

class account_delete_superuser(APIView):
      permission_classes = [IsAuthenticated,IsSuperAdmin]     
      def delete(self,request,pk):
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                  return Response({"details":"data not found"},status=403)
            if(user.role != User.SUPER_ADMIN):
                  return Response({"details":"This is for deleting super user only "},status=403)      
            if(user.pk == pk):
                 return Response({"Super Admin cannot delete himself"})   
            user.delete()
            return Response({"details":"Super Admin deleted successfully"},status=200)


class AccountAdminView(ModelViewSet):
    permission_classes = [IsAuthenticated,IsSuperAdminOrTenantAdmin]
    def get_serializer_class(self):
        if self.action  == 'create':
            return UserAdminSerializerCreate
        elif self.action in ['update','partial_update']:
            return UserEditSerializer
        return UserSerializerView
    
    def get_queryset(self):
        user = self.request.user
        if user.role == User.TENANT_ADMIN:
            return User.objects.filter(tenant = user.tenant,role = User.TENANT_ADMIN)
        return User.objects.filter(role = User.TENANT_ADMIN)    
    
    def destroy(self, request, *args, **kwargs):
         user = self.get_object()
         if user.pk == request.user.pk:
              return Response({"details":"Admin cannot delete himself"})
         return super().destroy(request, *args, **kwargs)
    

class AccountUserView(ModelViewSet):
    permission_classes = [IsAuthenticated,IsTenantAdminOrUser]
    def get_permissions(self):
         if self.action in ['create','destroy']:
              return [IsAuthenticated(),IsTenantAdmin()]     
         return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserSerializerCreate
        elif self.action in ['update','partial_update']:
            return UserEditSerializer
        return UserSerializerView
    
    def get_queryset(self):
        user = self.request.user
        if user.role == User.TENANT_ADMIN:
            return User.objects.filter(tenant = user.tenant)
        return User.objects.filter(pk = user.pk,tenant = user.tenant)
    
class AccountTenantView(RetrieveAPIView,GenericAPIView):
     permission_classes = [IsAuthenticated,IsSuperAdmin]
     serializer_class = UserSerializerView
    
     def retrieve(self, request, *args, **kwargs):
          pk = kwargs.get("pk")
          tenant = get_object_or_404( Tenant,  pk = pk )
          user = User.objects.filter(tenant = tenant).order_by('role')
          serializer = self.get_serializer(user,many=True)
          return Response(serializer.data)
     
           
      
class LoginView(TokenObtainPairView):
    serializer_class = EmailTokenSerializer
     