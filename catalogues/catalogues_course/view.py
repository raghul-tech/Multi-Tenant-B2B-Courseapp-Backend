from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.permission import UserRole,IsTenantActive,IsTenantAdmin
from catalogues.models import Catalogues_Courses,Catalogues
from .serializers import Catalogues_Course_Serializers
from course.models import Course_db
from catalogues.views import DefaultPagination
from rest_framework.generics import GenericAPIView

class Catalogue_Course_View(GenericAPIView):
    permission_classes = [IsAuthenticated,IsTenantActive]
    pagination_class = DefaultPagination
    serializer_class = Catalogues_Course_Serializers
    def get_queryset(self):
        user = self.request.user
        if user.role == UserRole.SUPER_ADMIN:
            return Catalogues_Courses.objects.all()
        elif user.role == UserRole.TENANT_ADMIN or user.role == UserRole.TENANT_USER:
            return  Catalogues_Courses.objects.filter(catalogue__tenant = user.tenant)
    def get(self,request):
        query = self.get_queryset()
        page = self.paginate_queryset(query)
        serializer = self.get_serializer(page,many=True)
        return self.get_paginated_response(serializer.data)

class Catalogue_Course_Create(APIView):
    permission_classes = [IsAuthenticated,IsTenantAdmin]
    def post(self,request):
        user = request.user
        try:
            course_id = request.data.get("course")
            catalog_id = request.data.get("catalogue")
            order = request.data.get("order")
        except:
            return Response({"details":"course id , catalogue id and order is required"},status=403)
        try:
             course = Course_db.objects.get(
                id = course_id,
                tenant = user.tenant,
                status = "PUBLISHED"
            )
             catalogue = Catalogues.objects.get(
                id = catalog_id,
                tenant = user.tenant
            )

        except Course_db.DoesNotExist or Catalogues.DoesNotExist:
             return Response({"details":"Course or catalogue not found"}, status =403)

        catalog, created = Catalogues_Courses.objects.get_or_create(
            order = order,
            catalogue = catalogue,
            course = course
        )
        if created:
           serializer = Catalogues_Course_Serializers(catalog)
           return Response(serializer.data,status=200)
        return Response({"details":"catalogue course already exists"},status=200)
    

class Catalogue_Course_Edit(APIView):
    permission_classes = [IsAuthenticated,IsTenantAdmin]
    def put(self,request,pk):
        user = request.user
        try:
            catalogcourse = Catalogues_Courses.objects.get(pk=pk,catalogue__tenant = user.tenant)
            catalog = Catalogues.objects.get(pk = catalogcourse.catalogue.pk)
        except Catalogues.DoesNotExist or Catalogues_Courses.DoesNotExist:
            return Response({"details":"Catalog is not found"},status=403)
        
        if catalog.tenant != user.tenant:
            return Response({"details":"Tenant can change only their Catalogous"})
        serializer = Catalogues_Course_Serializers(catalogcourse,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=403)
    
    def delete(self,request,pk):
        user = request.user
        try:
            catalog_course = Catalogues_Courses.objects.get(pk=pk,catalogue__tenant = user.tenant)
            catalog = Catalogues.objects.get(pk = catalog_course.catalogue.pk)
        except Catalogues.DoesNotExist  or Catalogues_Courses.DoesNotExist:
            return Response({"details":"Catalog is not found"},status=403)
        
        if catalog.tenant != user.tenant:
            return Response({"details":"Tenant can change only their Catalogous"})
        catalog_course.delete()
        return Response({"details":"catalogue course is deleted"},status=200)
    
        

    