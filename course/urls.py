from django.urls import path
from .views import Course_View,Course_Edit,Course_Details,Course_All,CourseCreate
from  .module.views import Module_View,Module_Edit,Module_Details,Module_Create
from .submodule.views import SubModule_View,SubModule_Edit,SubModule_Create

urlpatterns = [
    path('view/', Course_View.as_view(), name='course-view'),
    path('create/', CourseCreate.as_view(), name='course-create'),
    path('edit/<int:pk>/', Course_Edit.as_view(), name='course-edit'), 
    path('details/<int:pk>/',Course_Details.as_view(),name="course-details"),
    path('all/',Course_All.as_view(),name='Course-All'),
    path('module/view/',Module_View.as_view(),name="Module-view"),
    path('module/create/',Module_Create.as_view(),name="Module-create"),
    path("module/details/",Module_Details.as_view(),name="Module-Details"),
    path('module/edit/<int:pk>/',Module_Edit.as_view(),name="Module-edit"),
    path('module/submodule/view/',SubModule_View.as_view(),name ="SubModule-view"),
    path('module/submodule/create/',SubModule_Create.as_view(),name ="SubModule-create"),
    path('module/submodule/edit/<int:pk>/',SubModule_Edit.as_view(),name ="SubModule-edit"),

] 