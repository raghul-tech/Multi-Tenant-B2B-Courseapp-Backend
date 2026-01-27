from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from tenant.models import Tenant
from .serializers import UserSerializer, EmailTokenSerializer, UserEditSerializer,UserSerializerView
from rest_framework.permissions import IsAuthenticated
from core.permission import IsSuperAdmin,IsTenantAdmin,IsTenantActive
from rest_framework_simplejwt.views import TokenObtainPairView 
from validate_email_address import validate_email
 

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

            serializer = UserSerializer(super_user)
            return Response(serializer.data,status=200)

class account_delete_superuser(APIView):
      permission_classes = [IsAuthenticated,IsSuperAdmin]     
      def delete(self,request,pk):
            try:
                data =   User.objects.get(pk=pk)
            except User.DoesNotExist:
                  return Response({"details":"data not found"},status=403)
            if(data.role != User.SUPER_ADMIN):
                  return Response({"details":"This is for deleting super user only "},status=403)         
            data.delete()
            return Response({"details":"Super Admin deleted successfully"},status=200)


class accounts_create_admin(APIView):
       permission_classes = [IsAuthenticated,IsSuperAdmin]

       def post(self,request):
        tenant_id = request.data.get("tenant")
        if not tenant_id:
               return Response({"details":"tenant is required"},status=403)
        try:
         tenant  = Tenant.objects.get(id = tenant_id)
        except Tenant.DoesNotExist:
               return Response({"Tenant not found"},status=403)
               
        if not tenant.is_active:
          return Response({"detail": "Tenant is not active."}, status=403)
        
        if not validate_email(request.data.get('email')):
                  return Response({"email is not valid"},status=403)
        
        if User.objects.filter(email = request.data.get('email')).exists():
                  return Response({"Email already exist"},status=403)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                   tenant = tenant,
            )
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)



class accounts_create(APIView):
    permission_classes = [IsAuthenticated,IsTenantAdmin]

    def post(self, request):
        user = request.user
        data = request.data.copy() 
        if not validate_email(request.data.get('email')):
                  return Response({"email is not valid"},status=403)
        if User.objects.filter(email = request.data.get('email')).exists():
                  return Response({"Email already exist"},status=403)

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save(
                   tenant = user.tenant
            )
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

class accounts_detail(APIView):
      permission_classes = [IsAuthenticated,IsTenantActive]

      def get(self, request):     
            user = request.user
            if user.role == User.SUPER_ADMIN:
                    data = User.objects.all() 
            elif user.role == User.TENANT_ADMIN:         
                    data = User.objects.filter(tenant=user.tenant)     
            elif user.role == User.TENANT_USER:
                    data = User.objects.filter(id=user.id)
            else:
                    return Response({"detail": "You do not have permission to view this content."}, status=403)
            serializer = UserSerializerView(data, many=True)
            return Response(serializer.data)
       

class accounts_edit(APIView):
      permission_classes = [IsAuthenticated,IsTenantActive]
      def put(self, request,pk):
                
                user = request.user
                if User.objects.filter(email = request.data.get('email')).exists():
                  return Response({"Email already exist"},status=403)
                try:
                  if user.role == User.SUPER_ADMIN:
                              user = User.objects.get(pk=pk)
                  elif user.role == User.TENANT_ADMIN:
                              user = User.objects.get(pk=pk, tenant=user.tenant)
                  elif user.role == User.TENANT_USER:
                       user = User.objects.get(pk=pk, email = user)        
                except User.DoesNotExist:
                              return Response({"User does not exist"},status=403)
                serializer = UserEditSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=200)

           
      def delete(self, request, pk):
           user = request.user
           try:
            if user.role == User.SUPER_ADMIN:
                        user = User.objects.get(pk=pk)
            elif user.role == User.TENANT_ADMIN:
                        user = User.objects.get(pk=pk, tenant=user.tenant)
            else:
                  return Response({"detail": "You do not have permission to perform this action."}, status=403)
           except User.DoesNotExist:
                              return Response({"User does not exist"},status=403)
           user.delete()
           return Response({"details":"user deleted"},status=200)
        
 


           
      
class LoginView(TokenObtainPairView):
    serializer_class = EmailTokenSerializer
     