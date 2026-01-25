from django.db import models
from tenant.models import Tenant
from accounts.models import User
from course.models import Course_db,Module,SubModule

# Create your models here.
class Skills(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=225)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
         unique_together = ("name","tenant")


class CourseSkill(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE
    )
    skills = models.ForeignKey(
        Skills,
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course_db,
        on_delete=models.CASCADE
    )
    course_weight = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
         unique_together = ("skills","course")



class UserSkillProgress(models.Model):
        user = models.ForeignKey(
             User,
             on_delete=models.CASCADE
        )
        skills = models.ForeignKey(
             Skills,
             on_delete=models.CASCADE
        )
        tenant = models.ForeignKey(
             Tenant,
             on_delete=models.CASCADE
        )
        profeciency = models.PositiveIntegerField(default = 0)
        last_updated = models.DateTimeField(auto_now=True)
        class Meta:
             unique_together = ("user","skills")
