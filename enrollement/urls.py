from django.urls import path
from .views import Enrollement_Edit, Enrollement_View

urlpatterns = [
    path('view/', Enrollement_View.as_view(), name='enrollement-list'),
    path('edit/<int:pk>/', Enrollement_Edit.as_view(), name='enrollement-detail'),
]