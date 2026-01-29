from django.urls import path,include
from .views import TenantView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("tenantview",TenantView,basename="tenantview")


urlpatterns = [
  path("",include(router.urls))
]