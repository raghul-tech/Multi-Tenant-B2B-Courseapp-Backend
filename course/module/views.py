from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from course.models import Module,Course_db
from .serializers import ModuleSerializer,Module_Details_Serializer
from core.permission import IsTenantAdmin,IsTenantUser


class Module_View(APIView):
     permission_classes = [IsAuthenticated,IsTenantUser]
     def get(self, request):
         user = request.user

         if user.role == User.SUPER_ADMIN:
             data = Module.objects.all()
         elif user.role == User.TENANT_ADMIN:
             data = Module.objects.filter(course__tenant = user.tenant)             
         elif user.role == User.TENANT_USER:
             data = Module.objects.filter(
                 course__status = "PUBLISHED",
                 course__enrollements__user = user
             ).distinct()
         else:
             return Response({"details":"not allowed"},status = 403)

         serializer = ModuleSerializer(data,many= True)
         return Response(serializer.data,status = 200)
      
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

         serializer = ModuleSerializer(data = request.data)
         if serializer.is_valid():
             serializer.save(
                 course = course
             )
             return Response(serializer.data,status = 200)
         return Response({"details":"Serialize error"}, status = 403)
     
class Module_Edit(APIView):
    permission_classes = [IsAuthenticated,IsTenantAdmin]

    def put (self,request,pk):
        try:
             module = Module.objects.get(pk=pk)
        except ModuleNotFoundError:
            return Response({"details":"Primary Key not found"},status = 403)
        course = module.course
        user = request.user
        if user.role == User.SUPER_ADMIN:
            pass
        elif user.role == User.TENANT_ADMIN:
            if (course.tenant != user.tenant):
                return Response({"details":"Details not found"},status=403)
        else:
            return Response({"details":"Dont have access for it "},status=403)
        
            
        serializer = ModuleSerializer(module,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response({"details":"Error"},status=403)
    
    def delete(self,request,pk):
        user = request.user
        try:
            module = Module.objects.get(pk = pk)
        except ModuleNotFoundError:
            return Response({"details":"Error"},status=403)
        course = module.course

        if user.role == User.SUPER_ADMIN:
            pass
        elif user.role == User.TENANT_ADMIN:
            if(course.tenant != user.tenant):
                return Response({"details":"dont have access"},status=403)
        else:
             return Response({"details":"dont have access"},status=403)
        
        module.delete()
        return Response(status=200)

class Module_Details(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        if user.role == User.SUPER_ADMIN:
            module = Module.objects.all()
        elif user.role == User.TENANT_ADMIN:
            module = Module.objects.filter(course__tenant = user.tenant)
        elif user.role == User.TENANT_USER:
            module = Module.objects.filter(
                course__status = "PUBLISHED",
                course__enrollements__user = user
            )
        else:
            return Response({"details":"Access Denied"},status = 403)
        
        module_serializer = Module_Details_Serializer(module,many=True)
        return Response(module_serializer.data,status=200)
        
