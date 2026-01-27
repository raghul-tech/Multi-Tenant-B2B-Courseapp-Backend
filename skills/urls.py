from django.urls import path
from .views import Skills_View,Skills_Edit,Skills_Create
from .courseskill.views import CourseSkill_Create,CourseSkill_View,CourseSkill_Edit,CourseSkill_Course
from .userskillprogress.views import UserSkillProgress_View,UserSkillProgress_User

urlpatterns = [
    path("view/",Skills_View.as_view(),name="skills_view"),
    path("create/",Skills_Create.as_view(),name="skills_create"),
    path("edit/<int:pk>/",Skills_Edit.as_view(),name="skills_edit"),
    path("courseskills/view/",CourseSkill_View.as_view(),name="courseskill-view"),
    path("courseskills/view/<int:course>/",CourseSkill_Course.as_view(),name="courseskill-course"),
    path("courseskills/create/",CourseSkill_Create.as_view(),name="courseskill-create"),
    path("courseskills/edit/<int:pk>/",CourseSkill_Edit.as_view(),name="courseskill-edit"),
    path("userprogress/view/",UserSkillProgress_View.as_view(),name="userprogress-view"),
    path("userprogress/view/<int:pk>/",UserSkillProgress_User.as_view(),name="userprogress-user"),

]