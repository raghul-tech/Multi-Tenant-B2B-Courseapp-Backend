from django.urls import path
from .views import LoginView, accounts_create,  accounts_detail, accounts_edit,account_create_superuser,account_delete_superuser

urlpatterns = [
   path('create/superuser/',account_create_superuser.as_view(),name ='superuser-create'),
   path('create/superuser/edit/<int:pk>/',account_delete_superuser.as_view(),name ='superuser-delete'),
   path('create/',accounts_create.as_view(),name='accounts_create'),
   path('view/',accounts_detail.as_view(),name='accounts_detail'),
   path('edit/<int:pk>/',accounts_edit.as_view(),name='accounts_edit'),
   path('login/',LoginView.as_view(),name='token_obtain_pair'),
]

