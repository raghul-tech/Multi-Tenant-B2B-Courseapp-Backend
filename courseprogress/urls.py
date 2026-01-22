from django.urls import path

from .views import  CourseProgress_Create, CourseProgress_View
from .moduleprogress.views import moduleProgress_View
from .submoduleprogress.views import submoduleProgress_Edit,submoduleProgress_View

urlpatterns = [

    path("view/",  CourseProgress_View.as_view(),  name="course-progress-list"  ),
    path( "create/",  CourseProgress_Create.as_view(),  name="course-progress-create"  ),
    path( "modules/view/",  moduleProgress_View.as_view(),  name="module-progress-list"  ),
    path("submodules/view/", submoduleProgress_View.as_view(),  name="submodule-progress-list" ),
    path(  "submodules/<int:pk>/",  submoduleProgress_Edit.as_view(),  name="submodule-progress-edit" ),
]
