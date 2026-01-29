
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import TenantSerializer
from .models import Tenant
from core.permission import  IsSuperAdmin
from rest_framework.viewsets import ModelViewSet

# Create your views here.

class TenantView(ModelViewSet):
    permission_classes = [IsAuthenticated,IsSuperAdmin]
    serializer_class = TenantSerializer

    def get_queryset(self):
        return Tenant.objects.all()