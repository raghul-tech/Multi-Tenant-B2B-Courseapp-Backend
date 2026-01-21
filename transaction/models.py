from django.db import models
from course.models import Course_db
from accounts.models import User
from tenant.models import Tenant

# Create your models here.
class Transactions(models.Model):

    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

    status_choice =[
        ('SUCCESS','success'),
        ('FAILED','failed'),
        ('PENDING','pending'),
    ]

    course = models.ForeignKey(
        Course_db,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(max_digits=20,decimal_places=2)
    status = models.CharField(max_length=20,choices=status_choice)
    payment_mode = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Payment Initiations"

    def __str__(self):
        return f"{self.user} - {self.course} - {self.status}"



