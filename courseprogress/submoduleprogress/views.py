from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.permission import UserRole,IsTenantUser
from courseprogress.models import UserSubModuleProgress,UserCourseProgress,UserModuleProgress
from .serializers import submoduleProgress_view_serializers
from rest_framework.response import Response
from skills.userskillprogress.views import user_skill_progress
from course.models import SubModule
from django.shortcuts import get_object_or_404

# Create your views here.
class submoduleProgress_View(APIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self,user):
        if user.role == UserRole.SUPER_ADMIN:
            data = UserSubModuleProgress.objects.all()
        elif user.role == UserRole.TENANT_ADMIN:
            data = UserSubModuleProgress.objects.filter(tenant = user.tenant)
        else:
            data = UserSubModuleProgress.objects.filter(user = user)
        return data

    def get(self,request):
        data = self.get_queryset(request.user)
        serializer = submoduleProgress_view_serializers(data,many=True)
        return Response(serializer.data,status=200)


class submoduleProgress_Edit(APIView):
    permission_classes = [IsAuthenticated,IsTenantUser]
    def get_queryset(self,user,data):
        submodule_current = data.submodule
        submodule_order = submodule_current.order
        if submodule_order >1:
            previous_progress = UserSubModuleProgress.objects.filter(
                user = user,
                course = data.course,
                module = data.module,
                submodule__order = submodule_order -1
            ).first()
            if not previous_progress or not previous_progress.submodule_completed:
                return False
        return True
    
    def put(self,request,pk):
        user = request.user
        try:
         data= UserSubModuleProgress.objects.get(
                pk=pk,
                tenant = user.tenant
                )
        except UserSubModuleProgress.DoesNotExist:
            return Response({"details":"submodule progress not found"},status = 403)
        
        if not self.get_queryset(user,data):
            return Response({"details":"COmmplete the previous submodule"},status=403)
        
        progress = request.data.get("progress")
        is_complete = request.data.get("complete")

        if is_complete is True:
            progress = 100
        else:
         if progress is not None:
            progress = int(progress)
            if progress >= 100:
                progress = 100
                is_complete = True
            elif progress < 0:
                progress = 0
                is_complete = False
            else:        
              is_complete = False
         else:
              progress = 0
    

        if  progress is None:
            return Response({"progress value is required"})
        if  is_complete is None:
            return Response({"complete value is required"})
        data.submodule_progress = progress
        data.submodule_completed = is_complete
        data.save()

        user = request.user
        course = data.course
        module = data.module

        total_module_submodule =UserSubModuleProgress.objects.filter(
            user = user,
            course = course,
            module = module
        ).count()
        completed_module_submodule = UserSubModuleProgress.objects.filter(
            user = user,
            course = course,
             module = module,
              submodule_completed = True
        ).count()
        total_module_progress = (completed_module_submodule/total_module_submodule)*100
        
        UserModuleProgress.objects.update_or_create(
            user = user,
            course = course,
            module = module,
            defaults={
                "module_progress" : total_module_progress,
                "module_completed" : total_module_progress == 100
            }
        )

        total_module = UserModuleProgress.objects.filter(
            user = user,
            course = course
        ).count()
        completed_module = UserModuleProgress.objects.filter(
            user = user,
            course = course,
            module_completed = True
        ).count()
        total_course_progress = (completed_module/total_module)*100

        UserCourseProgress.objects.update_or_create(
            user = user,
            course = course,
            tenant = user.tenant,
            defaults={
                "course_progress" : total_course_progress,
                "course_completed" : total_course_progress == 100
            }
        )
        user_skill_progress(user,course,total_course_progress)

        return Response({
                "submodule_progress":data.submodule_progress,
                "module_progress" : total_module_progress,
                "module_completed" : total_module_progress == 100,
               "course_progress" : total_course_progress,
                "course_completed" : total_course_progress == 100
        })









             
    

        
        

