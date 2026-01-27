from django.db import models
from accounts.models import User
from tenant.models import Tenant
from course.models import Course_db,Module,SubModule

# Create your models here.
class UserCourseProgress(models.Model):
        user = models.ForeignKey(
                User,
                on_delete=models.CASCADE
        )
        tenant = models.ForeignKey(
                Tenant,
                on_delete=models.CASCADE
        )
        course = models.ForeignKey(
                Course_db,
                on_delete=models.CASCADE
        )
        last_updated = models.DateTimeField(auto_now=True)
        course_progress = models.PositiveIntegerField(default=0)
        course_completed = models.BooleanField(default = False)
        class Meta:
                unique_together = ("user","course")
    
class UserModuleProgress(models.Model):
        user = models.ForeignKey(
                User,
                on_delete=models.CASCADE
        )
        tenant = models.ForeignKey(
                Tenant,
                on_delete=models.CASCADE
        )
        course = models.ForeignKey(
                Course_db,
                on_delete=models.CASCADE
        )
        module = models.ForeignKey(
                Module,
                on_delete=models.CASCADE
        )
        last_updated = models.DateTimeField(auto_now=True)
        module_progress = models.PositiveIntegerField(default=0)
        module_completed = models.BooleanField(default = False)
        class Meta:
                unique_together = ("user","module")

class UserSubModuleProgress(models.Model):
        user = models.ForeignKey(
                User,
                on_delete=models.CASCADE
        )
        tenant = models.ForeignKey(
                Tenant,
                on_delete=models.CASCADE
        )
        course = models.ForeignKey(
                Course_db,
                on_delete=models.CASCADE
        )
        module = models.ForeignKey(
                Module,
                on_delete=models.CASCADE
        )
        submodule = models.ForeignKey(
                SubModule,
                on_delete=models.CASCADE
        )
        last_updated = models.DateTimeField(auto_now=True)
        submodule_progress = models.PositiveIntegerField(default=0)
        submodule_completed = models.BooleanField(default = False)
        class Meta:
                unique_together = ("user","submodule")


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    submodule_progress = models.OneToOneField(
        UserSubModuleProgress,
        on_delete=models.CASCADE
    )

    last_watched_duration = models.PositiveIntegerField(default=0)
    mark_scored = models.PositiveIntegerField(default=0)

    completed = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
