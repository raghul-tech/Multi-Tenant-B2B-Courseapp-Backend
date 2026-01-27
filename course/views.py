from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from .serializers import CourseSerializer,Course_Details_Serializer,CourseCreateSerializer,CourseEditSerializer
from .models import Course_db
from core.permission import IsTenantAdmin,IsTenantActive
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import GenericAPIView

# Create your views here.
class DefaultPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 50

class Course_View(GenericAPIView):
    permission_classes = [IsAuthenticated,IsTenantActive]
    pagination_class = DefaultPagination
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == User.SUPER_ADMIN:
            return Course_db.objects.all()
        elif user.role == User.TENANT_ADMIN:
            return Course_db.objects.filter(tenant=user.tenant)
        elif user.role == User.TENANT_USER:
            return Course_db.objects.filter(
                status = "PUBLISHED",
                enrollements__user = user
            )
    
    def get(self, request):
        query = self.get_queryset()
        page = self.paginate_queryset(query)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    

class CourseCreate(APIView):
    permission_classes = [IsAuthenticated,IsTenantAdmin]
    def post(self, request):        
        serializer = CourseCreateSerializer(data=request.data,context = {'request':request})
        serializer.is_valid(raise_exception=True)
        course=  serializer.save()
        return Response(CourseSerializer(course).data, status=201)
        
class Course_Edit(APIView):
    permission_classes = [IsAuthenticated,IsTenantAdmin]
    def put(self, request, pk):
        user = request.user
        try:
            course = Course_db.objects.get(pk=pk,tenant = user.tenant)
        except Course_db.DoesNotExist:
            return Response({"detail": "Course not found"}, status=404)     
            
        serializer = CourseEditSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():   
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    

    def delete(self, request, pk):
        user = request.user 
        try:
            course = Course_db.objects.get(pk=pk,tenant = user.tenant)
        except Course_db.DoesNotExist:
            return Response({"detail": "Course not found"}, status=404)
        
        course.delete()
        return Response({"details":"course deleted"},status=204)
    

class Course_Details(GenericAPIView):
    permission_classes = [IsAuthenticated,IsTenantActive]
    pagination_class = DefaultPagination
    serializer_class = Course_Details_Serializer

    def get_queryset(self,pk):
        user = self.request.user
        if user.role == User.SUPER_ADMIN:
            return Course_db.objects.all()
        elif user.role == User.TENANT_ADMIN:
            return Course_db.objects.filter(tenant = user.tenant)
        elif user.role == User.TENANT_USER:
            return Course_db.objects.filter(
                pk = pk,
                status = "PUBLISHED",
                enrollements__user = user
            )

    def get(self,request,pk):
        query = self.get_queryset(pk)
        page = self.paginate_queryset(query)
        serializer = self.get_serializer(page,many=True)
        return self.get_paginated_response(serializer.data)
    
class Course_All(GenericAPIView):
    permission_classes = [IsAuthenticated,IsTenantActive]
    pagination_class = DefaultPagination
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == User.SUPER_ADMIN:
            return Course_db.objects.all()
        elif user.role == User.TENANT_ADMIN:
            return Course_db.objects.filter(tenant = user.tenant)
        else:
            return  Course_db.objects.filter(
                tenant = user.tenant,
                status = "PUBLISHED"
            )

    def get(self,request):
        query = self.get_queryset()
        page = self.paginate_queryset(query)
        serializer = self.get_serializer(page,many=True)
        return self.get_paginated_response(serializer.data)
    
        


    
        


         
        

         
