from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.permission import UserRole,IsTenantActive
from skills.models import UserSkillProgress,CourseSkill
from .serializers import UserSkillProgress_View_Serializer
from rest_framework.response import Response
from courseprogress.models import UserCourseProgress

class UserSkillProgress_View(APIView):
    permission_classes = [IsAuthenticated,IsTenantActive]
    def get_queryset(self,user):
        if user.role == UserRole.SUPER_ADMIN:
            data = UserSkillProgress.objects.all()
        elif user.role == UserRole.TENANT_ADMIN:
            data = UserSkillProgress.objects.filter(tenant = user.tenant)
        else:
            data = UserSkillProgress.objects.filter(user = user)
        return data

    def get(self,request):
        data = self.get_queryset(request.user)
        serializer = UserSkillProgress_View_Serializer(data,many=True)
        return Response(serializer.data,status=200)


class UserSkillProgress_User(APIView):
    permission_classes = [IsAuthenticated,IsTenantActive]
    def get(self,request,pk):
        user = request.user
        if user.role == UserRole.SUPER_ADMIN:
            data = UserSkillProgress.objects.filter(user=pk)
        elif user.role == UserRole.TENANT_ADMIN:
            data = UserSkillProgress.objects.filter(user=pk,tenant = user.tenant)
        else:
            return Response({"details":"Not Authorized"},status=403)
        serializer = UserSkillProgress_View_Serializer(data,many=True)
        return Response(serializer.data,status=200)


    
         
def user_skill_progress(user, course, course_progress_percent):

    course_skills = CourseSkill.objects.filter(course=course)

    for cs in course_skills:
        skill = cs.skills
       # weight = cs.course_weight
       # contribution = (course_progress_percent / 100) * weight
        userskill, _ = UserSkillProgress.objects.get_or_create(
            user=user,
            skills=skill,
            tenant=user.tenant,
            defaults={"profeciency": 0}
        )
        userskill.profeciency = skill_proficiency(
            user=user,
            skill=skill
        )
        userskill.save()

def skill_proficiency(user, skill):

    total = 0

    course_skills = CourseSkill.objects.filter(
        skills=skill,
        course__usercourseprogress__user=user
    ).select_related("course")

    for cs in course_skills:
        course_progress = UserCourseProgress.objects.filter(
            user=user,
            course=cs.course
        ).values_list("course_progress", flat=True).first() or 0

        total += (course_progress / 100) * cs.course_weight

    return min(int(total), 100)

