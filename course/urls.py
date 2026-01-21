from django.urls import path
from .views import Course_View,Course_Edit,Course_Details
from  .module.views import Module_View,Module_Edit,Module_Details
from .submodule.views import SubModule_View,SubModule_Edit
from .submodule_videoprogress.views import Videoprogress_View,Videoprogress_Edit

urlpatterns = [
    path('view/', Course_View.as_view(), name='course-view'),
    path('edit/<int:pk>/', Course_Edit.as_view(), name='course-edit'),
    path('details/',Course_Details.as_view(),name="course-details"),
    path('module/view/',Module_View.as_view(),name="Module-view"),
    path("module/details/",Module_Details.as_view(),name="Module-Details"),
    path('module/edit/<int:pk>/',Module_Edit.as_view(),name="Module-edit"),
    path('module/submodule/view/',SubModule_View.as_view(),name ="SubModule-view"),
    path('module/submodule/edit/<int:pk>/',SubModule_Edit.as_view(),name ="SubModule-edit"),
    path('module/submodule/videoprogress/view/',Videoprogress_View.as_view(),name = "subModule-Videoprogress"),
    path('module/submodule/videoprogress/edit/<int:pk>/',Videoprogress_Edit.as_view(),name = "subModule-Videoprogress-edit")

] 