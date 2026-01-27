from django.urls import path

from .views import  CourseProgress_View
from .moduleprogress.views import moduleProgress_View
from .submoduleprogress.views import submoduleProgress_View
from  .userprogress.views import UserProgressView,UserProgressEdit

urlpatterns = [

    path("view/",  CourseProgress_View.as_view(),  name="course-progress-list"  ),
    path( "modules/view/",  moduleProgress_View.as_view(),  name="module-progress-list"  ),
    path("submodules/view/", submoduleProgress_View.as_view(),  name="submodule-progress-list" ),
    path("userprogress/view/",UserProgressView.as_view(),name="userprogress-view"),
    path('userprogress/edit/<int:pk>/',UserProgressEdit.as_view(),name="userprogress-edit")
]
