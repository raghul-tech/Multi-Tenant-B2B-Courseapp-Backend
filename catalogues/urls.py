from django.urls import path
from .views import Catalogues_View,Catalogues_Edit,Catalogues_Details,Catalogues_Create
from .catalogues_course.view import Catalogue_Course_View,Catalogue_Course_Edit,Catalogue_Course_Create

urlpatterns =[
        path("view/",Catalogues_View.as_view(),name="catalogue-view"),
         path("create/",Catalogues_Create.as_view(),name="catalogue-create"),
        path("edit/<int:pk>/",Catalogues_Edit.as_view(),name="catalogue-edit"),
        path("details/",Catalogues_Details.as_view(),name="catalogue-details"),
        path("courses/view/",Catalogue_Course_View.as_view(),name="catalogue-course-view"),
         path("courses/create/",Catalogue_Course_Create.as_view(),name="catalogue-course-create"),
        path("courses/edit/<int:pk>/",Catalogue_Course_Edit.as_view(),name="catalogue-course-edit")
]