from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.permission import UserRole,IsTenantActive,IsTenantUser
from courseprogress.models import UserProgress,UserSubModuleProgress,UserCourseProgress,UserModuleProgress
from .serializers import UserProgressSerializers,UserProgressEditSerializer
from rest_framework.response import Response
from skills.userskillprogress.views import user_skill_progress
from django.shortcuts import get_object_or_404
from course.models import Module,SubModule

class UserProgressView(APIView):
    permission_classes = [IsAuthenticated,IsTenantActive]
    def get_queryset(self,user):
        if user.role == UserRole.SUPER_ADMIN:
            data = UserProgress.objects.all()
        elif user.role == UserRole.TENANT_ADMIN:
            data = UserProgress.objects.filter( submodule_progress__tenant = user.tenant)
        elif user.role == UserRole.TENANT_USER:
            data = UserProgress.objects.filter(user = user)
        return data

    def get(self,request):
        data = self.get_queryset(request.user)
        serializer = UserProgressSerializers(data,many=True)
        return Response(serializer.data,status=200)
    



class UserProgressEdit(APIView):
   permission_classes=[IsAuthenticated,IsTenantUser]
   def put(self, request, pk):
    user = request.user

    progress = get_object_or_404(
        UserProgress,
        pk=pk,
        user=user
    )
    if not self.previous_module_complete(user,progress.submodule_progress.module):
        return Response({"details":"Finish the prevoius module first"},status=403)
    if not self.prevoius_submodule_complete(user,progress.submodule_progress.submodule):
        return Response({"details":"Finish the prevoius submodule first"},status=403)

    serializer = UserProgressEditSerializer(
        progress,
        data=request.data,
        partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    submodule = progress.submodule_progress.submodule

    if submodule.submodule_type == "VIDEO":
        percent = (
            progress.last_watched_duration / submodule.video_duration
        ) * 100

    else:
        percent = (
            progress.mark_scored / submodule.assignment_mark
        ) * 100

    percent = min(int(percent), 100)

    progress.completed = percent == 100
    progress.save()

    sub_progress = progress.submodule_progress
    sub_progress.submodule_progress = percent
    sub_progress.submodule_completed = percent == 100
    sub_progress.save()


    self.update_module_and_course_progress(user, sub_progress)

    return Response({
        "submodule_progress": percent,
        "completed": percent == 100
    })
   
   def previous_module_complete(self,user, current_module):
           
            if current_module.order == 1:
                return True

            previous_module = Module.objects.filter(
                course=current_module.course,
                order=current_module.order - 1
            ).first()

            if not previous_module:
                return False 
            previous_progress = UserModuleProgress.objects.filter(
                user=user,
                tenant=user.tenant,
                module=previous_module,
                module_completed=True
            ).exists()
            return previous_progress
   
   def prevoius_submodule_complete(self,user, current_sub):

            if current_sub.order == 1:
                return True

            previous_sub = SubModule.objects.filter(
                module=current_sub.module,
                order=current_sub.order - 1
            ).first()

            if not previous_sub:
                return False 
            previous_progress = UserSubModuleProgress.objects.filter(
                user=user,
                tenant=user.tenant,
                submodule=previous_sub,
                submodule_completed=True
            ).exists()
            return previous_progress

   def  update_module_and_course_progress(self,user,sub_progress):
        course = sub_progress.course
        module = sub_progress.module
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