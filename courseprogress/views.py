from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.permission import UserRole,IsTenantActive
from .models import UserCourseProgress,UserSubModuleProgress,UserModuleProgress,UserProgress
from .serializers import courseprogress_view_serializers
from rest_framework.response import Response

# Create your views here.
class CourseProgress_View(APIView):
    permission_classes = [IsAuthenticated,IsTenantActive]
    def get_queryset(self,user):
        if user.role == UserRole.SUPER_ADMIN:
            data = UserCourseProgress.objects.all()
        elif user.role == UserRole.TENANT_ADMIN:
            data = UserCourseProgress.objects.filter(tenant = user.tenant)
        elif user.role == UserRole.TENANT_USER:
            data = UserCourseProgress.objects.filter(user = user)
        return data 

    def get(self,request):
        data = self.get_queryset(request.user)
        serializer = courseprogress_view_serializers(data,many=True)
        return Response(serializer.data,status=200)
    
def initialize_course_progress(user, course):
    UserCourseProgress.objects.get_or_create(
            user=user,
            tenant=user.tenant,
            course=course,
            course_completed=False,
            course_progress=0
        )

    modules = course.modules.all()

    for module in modules:
        UserModuleProgress.objects.get_or_create(
                user=user,
                tenant=user.tenant,
                course=course,
                module=module,
                defaults={
                    "module_progress": 0, 
                    "module_completed": False
                }
        )

        submodules = module.submodules.all()

        for submodule in submodules:
           submodule_progress, _ =  UserSubModuleProgress.objects.get_or_create(
                user=user,
                tenant=user.tenant,
                course=course,
                module=module,
                submodule=submodule,
                defaults={
                    "submodule_progress": 0,
                    "submodule_completed": False
                }
            )
           UserProgress.objects.get_or_create(
               user = user,
               submodule_progress = submodule_progress,
           )



