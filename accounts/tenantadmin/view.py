from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.permission import IsSuperAdminOrTenantAdmin
from .serializers import UserAdminCreateSerializer, UserAdminViewSerializer, UserAdminEditSerializer
from accounts.models import User

class AccountAdminView(ModelViewSet):
    permission_classes = [IsAuthenticated,IsSuperAdminOrTenantAdmin]
    def get_serializer_class(self):
        if self.action  == 'create':
            return UserAdminCreateSerializer 
        if self.action in ['update','partial_update']:
            return UserAdminEditSerializer
        return UserAdminViewSerializer
    def get_queryset(self):
        user = self.request.user
        if user.role == User.TENANT_ADMIN:
            return User.objects.filter(tenant = user.tenant)
        return User.objects.filter(role = User.TENANT_ADMIN)
    
    
    