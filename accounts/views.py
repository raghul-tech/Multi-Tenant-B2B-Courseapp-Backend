from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from tenant.models import Tenant
from .serializers import UserSerializer, EmailTokenSerializer
from rest_framework.permissions import IsAuthenticated
from core.permission import IsTenantAdmin,IsTenantUser,IsSuperAdmin
from rest_framework_simplejwt.views import TokenObtainPairView 

 

# Create your views here.
class account_create_superuser(APIView):
      permission_classes = [IsAuthenticated,IsSuperAdmin]
      def post(self,request):
            user = request.user
            if user.role != User.SUPER_ADMIN:
                  return Response({"details":"Not Authroized"},status=404)
            email = request.data.get("email")
            passwd = request.data.get("password")

            if not email or not passwd:
                  return Response({"details":"email and password is required"},status=400)

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
            user = request.user
            if user.role != User.SUPER_ADMIN:
                  return Response({"details":"Only super admin can delete a super admin"},status=403)
            if(data.role != User.SUPER_ADMIN):
                  return Response({"details":"This is for deleting super user only "},status=403)
             
            
            data.delete()
            return Response({"details":"Super Admin deleted successfully"},status=200)



class accounts_create(APIView):
    permission_classes = [IsAuthenticated,IsTenantAdmin]

    def post(self, request):
        current_user = request.user
        data = request.data.copy() 

        tenant_isActive  = Tenant.objects.get(id=data.get("tenant")).is_active

        if not tenant_isActive:
          return Response({"detail": "Tenant is not active."}, status=403)

        if current_user.role == User.SUPER_ADMIN:
            serializer = UserSerializer(data=data)
        elif current_user.role == User.TENANT_ADMIN:
            if( data.get("role") != User.TENANT_USER):
                  return Response(
                      {"detail": "Tenant Admins can only create Tenant Users."},
                      status=status.HTTP_403_FORBIDDEN )
            if(data.get("tenant") != current_user.tenant.id):
                  return Response(
                      {"detail": "Tenant Admins can only create users within their own tenant."},
                      status=status.HTTP_403_FORBIDDEN )

            serializer = UserSerializer(data=data)

        else:
            return Response(
                {"detail": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN
            )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

class accounts_detail(APIView):
      permission_classes = [IsAuthenticated,IsTenantUser]

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
            serializer = UserSerializer(data, many=True)
            return Response(serializer.data)
       

class accounts_edit(APIView):
      permission_classes = [IsAuthenticated,IsTenantUser]
      def put(self, request,pk):
                
                user = request.user
                if user.role == User.SUPER_ADMIN:
                        user = User.objects.get(pk=pk)
                elif user.role == User.TENANT_ADMIN:
                        user = User.objects.get(pk=pk, tenant=user.tenant)
                elif user.role == User.TENANT_USER and user.pk == pk:
                        user = User.objects.get(pk=pk)
                else:
                    return Response({"detail": "You do not have permission to perform this action."}, status=403)
                serializer = UserSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save( )
                    return Response(serializer.data)

           
      def delete(self, request, pk):
           user = request.user
           if user.role == User.SUPER_ADMIN:
                    user = User.objects.get(pk=pk)
           elif user.role == User.TENANT_ADMIN:
                    user = User.objects.get(pk=pk, tenant=user.tenant)
           else:
                return Response({"detail": "You do not have permission to perform this action."}, status=403)
           user.delete()
           return Response(status=204)
        
 


           
      
class LoginView(TokenObtainPairView):
    serializer_class = EmailTokenSerializer
     