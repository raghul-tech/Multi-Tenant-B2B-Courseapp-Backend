from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import EnrollementSerializer
from rest_framework.response import Response
from .models import Enrollement
from core.permission import UserRole as User
from course.models import Course_db

# Create your views here.
class Enrollement_View(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == User.SUPER_ADMIN:
            data = Enrollement.objects.all()
        elif user.role == User.TENANT_ADMIN:
            data = Enrollement.objects.filter(course__tenant = user.tenant)
        elif user.role == User.TENANT_USER:
            data = Enrollement.objects.filter(user = user)
        else:
            return Response({"detail": "Not allowed"}, status=403)
        
        serializer = EnrollementSerializer(data, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request):
        user = request.user
        if user.role == User.SUPER_ADMIN:
            return Response({"details":"Suoer Admin can't assign Course" }, status=400)
        course_id = request.data.get("course")
        user_id = request.data.get("user")
        if not course_id or not user_id:
            return Response({"details":"course and user id is required"},status=400)
        try:
          enrollements=    Enrollement.objects.get(
                user = user_id,
                tenant = user.tenant
            )
          course =   Course_db.objects.get(
                course = course_id,
               tenant = user.tenant
            )
        except Enrollement.DoesNotExist or Course_db.DoesNotExist:
            return Response({"details":"enrollememts or course DB not found "},status = 400)
        
        if enrollements.role in [
            User.SUPER_ADMIN,
            User.TENANT_ADMIN
        ]:
             return Response(
                {"detail": "Course cannot be assigned to admin users"},
                status=400
            )

        if not enrollements.is_active:
            return Response(
                {"detail": "User is not active"},
                status=400
            )

        if user.role == User.TENANT_USER:
            if enrollements.user != user:
                return Response({"details":"Tenant User cant assign course to others"},status=400)
            enrolled = True
        else:
            enrolled = False

        enroll, created = Enrollement.objects.get_or_create(
            user = enrollements,
            course = course,
            defaults={
                "assigned_by":user,
                "self_assigned":enrolled
            }

        )
        if not created:
            return Response({"details":"Enrollements already exist"},status=200)
        
        serializer = EnrollementSerializer(enroll)
        return Response(serializer.data,status=200)


      
        
    
class Enrollement_Edit(APIView):
    permission_classes = [IsAuthenticated]

    def put(self,request,pk):
        user = request.user
        try:
            enrollement = Enrollement.objects.get(pk=pk)
        except Enrollement.DoesNotExist:
            return Response({"detail":"Enrollement not found"}, status=404)
        
        if user.role == User.SUPER_ADMIN:
             serializer = EnrollementSerializer(enrollement, data=request.data, partial=True)
        elif user.role == User.TENANT_ADMIN:
            if(enrollement.course.tenant != user.tenant):
                return Response({"detail":"Not allowed"}, status=403)
            else:
                 serializer = EnrollementSerializer(enrollement, data=request.data, partial=True)
        elif user.role == User.TENANT_USER:
            if(enrollement.user != user):
                return Response({"detail":"Not allowed"}, status=403)
            else:
                allowed_fields = {
                    "status": request.data.get("status")
                }
                serializer = EnrollementSerializer(enrollement, data=allowed_fields, partial=True)
                
        else:   
            return Response({"detail":"Not allowed"}, status=403)
        
       
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        user = request.user
        try:
            enrollement = Enrollement.objects.get(pk=pk)
        except Enrollement.DoesNotExist:
            return Response({"detail":"Enrollement not found"}, status=404)
        if user.role == User.SUPER_ADMIN:
            pass
        elif user.role == User.TENANT_ADMIN:
            if(enrollement.course.tenant != user.tenant):
                return Response({"detail":"Not allowed"}, status=403)
        else:   
            return Response({"detail":"Not allowed"}, status=403)
        enrollement.delete()
        return Response({"detail":"Enrollement deleted"}, status=200)
    
