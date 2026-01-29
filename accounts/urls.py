from django.urls import path,include
from .views import LoginView,account_create_superuser,account_delete_superuser,AccountAdminView,AccountUserView,AccountTenantView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("tenantadmin",AccountAdminView,basename="tenantadmin")
router.register("tenantuser",AccountUserView,basename="tenantuser")

urlpatterns = [
   path('create/superuser/',account_create_superuser.as_view(),name ='superuser-create'),
   path('create/superuser/delete/<int:pk>/',account_delete_superuser.as_view(),name ='superuser-delete'),
   path('tenantview/<int:pk>/',AccountTenantView.as_view(),name="tenantview"),
   path('login/',LoginView.as_view(),name='token_obtain_pair'),

   path('',include(router.urls)),
]

