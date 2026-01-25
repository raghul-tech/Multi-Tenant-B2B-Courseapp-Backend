from django.db import models
from accounts.models import User
from course.models import Course_db

# Create your models here.
class Enrollement(models.Model):

    ENROLLED = 'ENROLLED'
    COMPLETED='COMPLETED'
    ASSIGNED= 'ASSIGNED'
     
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        Course_db,
        on_delete=models.CASCADE,
        related_name="enrollements"
    )
    assigned_by = models.ForeignKey(
        User,   
        on_delete=models.CASCADE,
        related_name='assigned_enrollements',
        null=True,  
    )

    STATUS_CHOICES = [
        ('ENROLLED', 'Enrolled'),
        ('COMPLETED', 'Completed'),
        ('ASSIGNED', 'Assigned'),
    ]

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='ASSIGNED')

    enrolled_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    self_enrolled = models.BooleanField(default = False)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user} - {self.course.title} - {self.status}"
