from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.permission import UserRole,IsTenantActive
from courseprogress.models import UserSubModuleProgress
from .serializers import submoduleProgress_view_serializers
from rest_framework.response import Response

# Create your views here.
class submoduleProgress_View(APIView):
    permission_classes = [IsAuthenticated,IsTenantActive]
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
