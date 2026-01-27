from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.SUPER_ADMIN


class IsTenantAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.TENANT_ADMIN and request.user.tenant.is_active


class IsTenantUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.TENANT_USER and request.user.tenant.is_active
    
class IsTenantActive(BasePermission):
    def has_permission(self, request, view):
        return  request.user.is_authenticated and request.user.role == UserRole.SUPER_ADMIN or request.user.tenant.is_active 


class UserRole():
    SUPER_ADMIN = "SUPER_ADMIN"
    TENANT_ADMIN = "TENANT_ADMIN"
    TENANT_USER = "TENANT_USER"