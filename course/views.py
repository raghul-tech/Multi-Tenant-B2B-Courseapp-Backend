from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from .serializers import CourseSerializer,Course_Details_Serializer
from .models import Course_db

# Create your views here.
class Course_View(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user

        if user.role == User.SUPER_ADMIN:
            data = Course_db.objects.all()
        elif user.role == User.TENANT_ADMIN:
            data = Course_db.objects.filter(tenant=user.tenant)
        elif user.role == User.TENANT_USER:
            data = Course_db.objects.filter(
                status = "PUBLISHED",
                enrollements__user = user
            )
        else:
            return Response({"detail": "Not allowed"}, status=403)
        
        serializer = CourseSerializer(data, many=True)
        return Response(
            serializer.data, status=200)
        
    
    def post(self, request):
        user  = request.user
        
        if user.role != User.TENANT_ADMIN:
            return Response({"detail": "Tenant Admin required"}, status=403)
        
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                tenant=user.tenant,
                created_by=user
            )
            return Response(serializer.data, status=201)
        
class Course_Edit(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        user = request.user
        try:
            course = Course_db.objects.get(pk=pk)
        except Course_db.DoesNotExist:
            return Response({"detail": "Course not found"}, status=404)     

        if user.role == User.SUPER_ADMIN:
            pass
        elif user.role == User.TENANT_ADMIN:
            if(course.tenant != user.tenant):
                return Response({"detail": "Not allowed"}, status=403)
        else:   
            return Response({"detail": "Not allowed"}, status=403)
             
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():   
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    

    def delete(self, request, pk):
        user = request.user 
        try:
            course = Course_db.objects.get(pk=pk)
        except Course_db.DoesNotExist:
            return Response({"detail": "Course not found"}, status=404)
        
        if user.role == User.SUPER_ADMIN:
            pass
        elif user.role == User.TENANT_ADMIN:
            if(course.tenant != user.tenant):
                return Response({"detail": "Not allowed"}, status=403)
        else:
            return Response({"detail": "Not allowed"}, status=403)
        
        course.delete()
        return Response(status=204)
    

class Course_Details(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user

        if user.role == User.SUPER_ADMIN:
            course = Course_db.objects.all()
        elif user.role == User.TENANT_ADMIN:
            course = Course_db.objects.filter(tenant = user.tenant)
        elif user.role == User.TENANT_USER:
            course = Course_db.objects.filter(
                status = "PUBLISHED",
                enrollements__user = user
            )
        else:
            return Response({"details":"Access denied"},status=403)
        
        course_serializer = Course_Details_Serializer(course,many=True)
        return Response(course_serializer.data,status=200)
    
        


         
        

         
