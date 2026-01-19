from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'SUPER_ADMIN'


class IsTenantAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'TENANT_ADMIN' or request.user.role == 'SUPER_ADMIN')


class IsTenantUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'TENANT_USER' or request.user.role == 'TENANT_ADMIN' or request.user.role == 'SUPER_ADMIN')

class UserRole():
    SUPER_ADMIN = "SUPER_ADMIN"
    TENANT_ADMIN = "TENANT_ADMIN"
    TENANT_USER = "TENANT_USER"