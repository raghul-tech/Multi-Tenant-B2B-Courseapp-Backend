from django.urls import path
from .views import TenantDashboard


urlpatterns = [
  path('view/', TenantDashboard.as_view(), name='tenant_dashboard'),
  path('edit/<int:pk>/', TenantDashboard.as_view(), name='tenant_detail'),
]