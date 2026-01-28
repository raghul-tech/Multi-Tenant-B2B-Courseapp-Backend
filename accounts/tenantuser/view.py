from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.permission import IsTenantAdminOrUser
from .serializers import UserSerializerCreate,UserSerializerEdit,UserSerializerView
from accounts.models import User

class AccountUserView(ModelViewSet):
    permission_classes = [IsAuthenticated,IsTenantAdminOrUser]
    def get_serializer_class(self):
        if self.action == 'create':
            return UserSerializerCreate
        elif self.action in ['update','partial_update']:
            return UserSerializerEdit
        return UserSerializerView
    def get_queryset(self):
        user = self.request.user
        if user.role == User.TENANT_ADMIN:
            return User.objects.filter(tenant = user.tenant)
        return User.objects.filter(pk = user.pk,tenant = user.tenant)
    
