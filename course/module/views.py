from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from course.models import Module,Course_db
from .serializers import ModuleSerializer,Module_Details_Serializer,ModuleCreateSerializer,ModuleEditSerializer
from core.permission import IsTenantAdmin,IsTenantActive
from rest_framework.generics import GenericAPIView
from course.views import DefaultPagination


class Module_View(GenericAPIView):
     permission_classes = [IsAuthenticated,IsTenantActive]
     pagination_class = DefaultPagination
     serializer_class = ModuleSerializer
     
     def get_query(self):
         user = self.request.user
         if user.role == User.SUPER_ADMIN:
             return Module.objects.all()
         elif user.role == User.TENANT_ADMIN:
             return Module.objects.filter(course__tenant = user.tenant)             
         elif user.role == User.TENANT_USER:
             return Module.objects.filter(
                 course__status = "PUBLISHED",
                 course__enrollements__user = user
             )

     def get(self, request):
         query = self.get_query()
         page = self.paginate_queryset(query)
         serializer = self.get_serializer(page,many=True)
         return self.get_paginated_response(serializer.data)



class Module_Create(APIView):
     permission_classes = [IsAuthenticated,IsTenantAdmin]
     def post(self,request):
         user = request.user

         if user.role != User.TENANT_ADMIN:
             return Response({"detail":"Tenant admin required to add a module"},status = 403)
         
         course_id = request.data.get("course")
         try:
            course = Course_db.objects.get(
                id = course_id,
                tenant = user.tenant
            )
         except Course_db.DoesNotExist:
             return Response({"details":"Course not found"}, status = 403)

         serializer = ModuleCreateSerializer(data = request.data)
         if serializer.is_valid():
             serializer.save(
                 course = course
             )
             return Response(serializer.data,status = 200)
         return Response(serializer.errors, status = 403)
     
class Module_Edit(APIView):
    permission_classes = [IsAuthenticated,IsTenantAdmin]

    def put (self,request,pk):
        try:
             module = Module.objects.get(pk=pk,course__tenant = request.user.tenant)
        except ModuleNotFoundError:
            return Response({"details":"Primary Key not found"},status = 403)            
        serializer = ModuleEditSerializer(module,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=403)
    
    def delete(self,request,pk):
        user = request.user
        try:
            module = Module.objects.get(pk = pk,course__tenant = user.tenant)
        except ModuleNotFoundError:
            return Response({"details":"Error"},status=403)
        module.delete()
        return Response({'Module is deleted'},status=200)


class Module_Details(GenericAPIView):
    permission_classes = [IsAuthenticated,IsTenantActive]
    pagination_class = DefaultPagination
    serializer_class = Module_Details_Serializer

    def get_queryset(self):
        user = self.request.user
        if user.role == User.SUPER_ADMIN:
            return Module.objects.all()
        elif user.role == User.TENANT_ADMIN:
            return Module.objects.filter(course__tenant = user.tenant)
        elif user.role == User.TENANT_USER:
            return Module.objects.filter(
                course__status = "PUBLISHED",
                course__enrollements__user = user
            )

    def get(self,request):
        query = self.get_queryset()
        page = self.paginate_queryset(query)
        serializer = self.get_serializer(page,many=True)
        return self.get_paginated_response(serializer.data)
        
