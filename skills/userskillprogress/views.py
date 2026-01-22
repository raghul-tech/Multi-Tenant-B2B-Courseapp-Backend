from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.permission import UserRole,IsTenantUser
from skills.models import UserSkillProgress,CourseSkill,Skills
from .serializers import UserSkillProgress_View_Serializer,UserSkillProgress_Create_Serializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from enrollement.models import Enrollement
from course.models import Course_db

class UserSkillProgress_View(APIView):
    permission_classes = [IsAuthenticated]
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
    
         
def user_skill_progress(user,course,completed):

    courseskill = CourseSkill.objects.filter(
        course = course
    )
    for cs in courseskill:
        skill = cs.skills
        weight = cs.course_weight

    progress = (completed/100)*weight

    userskill,created = UserSkillProgress.objects.get_or_create(
        user = user,
        skills = skill,
        tenant = user.tenant,
        defaults={
            "profeciency":0
        }
    )
    userskill.profeciency += progress
    userskill.save()