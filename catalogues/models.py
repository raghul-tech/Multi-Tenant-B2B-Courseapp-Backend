from django.db import models
from accounts.models import User
from tenant.models import Tenant
from course.models import Course_db

# Create your models here.
class Catalogues(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="Catalogues_User"
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="Catalogues_Tenant"
    )
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ["tenant","name"]

class Catalogues_Courses(models.Model):
    catalogue = models.ForeignKey(
        Catalogues,
        on_delete=models.CASCADE,
        related_name="catalogue_id"
    )
    course = models.ForeignKey(
        Course_db,
        on_delete=models.CASCADE,
        related_name="catalogue_course"
    )
    orders = models.PositiveIntegerField()

    class Meta:
        unique_together = ["course","catalogue"]
        ordering = ["orders"]



