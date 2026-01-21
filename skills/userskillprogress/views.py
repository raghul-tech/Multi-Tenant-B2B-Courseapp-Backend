from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.permission import UserRole,IsTenantUser
from skills.models import UserSkillProgress
from .serializers import UserSkillProgress_View_Serializer,UserSkillProgress_Create_Serializer
from rest_framework.response import Response

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
    
class UserSkillProgress_Create(APIView):
        permission_classes = [IsAuthenticated,IsTenantUser]
        def post(self,request):
          serializer = UserSkillProgress_Create_Serializer(
             request.data,
             context = {"request":request}
          )
          serializer.is_valid(raise_exception=True)
          serializer.save()
          return Response(serializer.data,status=201)








    