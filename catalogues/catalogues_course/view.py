from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.permission import UserRole
from catalogues.models import Catalogues_Courses,Catalogues
from .serializers import Catalogues_Course_Serializers
from course.models import Course_db

class Catalogue_Course_View(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        if user.role == UserRole.SUPER_ADMIN:
            data = Catalogues_Courses.objects.all()
        elif user.role == (UserRole.TENANT_ADMIN or user.role == UserRole.TENANT_USER):
            data = Catalogues_Courses.objects.filter(catalogue__tenant = user.tenant)
        else:
            return Response({"details":"Not authorized"},status=403)
        serializer = Catalogues_Course_Serializers(data,many=True)
        return Response(serializer.data,status=200)
    
    def post(self,request):
        user = request.user
        if user.role != UserRole.TENANT_ADMIN:
            return Response({"details":"Tenant Admin can only create catalogue course"},status=403)
        course_id = request.data.get("course")
        catalog_id = request.data.get("catalogue")
        try:
             course = Course_db.objects.get(
                id = course_id,
                tenant = user.tenant
            )
             catalogue = Catalogues.objects.get(
                id = catalog_id,
                tenant = user.tenant
            )

        except Course_db.DoesNotExist or Catalogues.DoesNotExist:
             return Response({"details":"Course or catalogue not found"}, status =403)

        catalog, created = Catalogues_Courses.objects.get_or_create(
            orders = request.data.get("orders"),
            catalogue = catalogue,
            course = course
        )
        if created:
           serializer = Catalogues_Course_Serializers(catalog)
           return Response(serializer.data,status=200)
        return Response({"details":"catalogue course not created"},status=403)
    

class Catalogue_Course_Edit(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request,pk):
        user = request.user
        if user.role != UserRole.TENANT_ADMIN:
            return Response({"details":"Tenant Admin can only edit"})
        try:
            catalogcourse = Catalogues_Courses.objects.get(pk=pk)
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
        if user.role != UserRole.TENANT_ADMIN:
            return Response({"details":"Tenant Admin can only edit"})
        try:
            catalog_course = Catalogues_Courses.objects.get(pk=pk)
            catalog = Catalogues.objects.get(pk = catalog_course.catalogue.pk)
        except Catalogues.DoesNotExist  or Catalogues_Courses.DoesNotExist:
            return Response({"details":"Catalog is not found"},status=403)
        
        if catalog.tenant != user.tenant:
            return Response({"details":"Tenant can change only their Catalogous"})
        catalog_course.delete()
        return Response({"details":"catalogue course is deleted"},status=403)
    
        

    