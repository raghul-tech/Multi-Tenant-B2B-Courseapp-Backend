from django.db import models
from tenant.models import Tenant
from accounts.models import User

# Create your models here.
class Course_db(models.Model):
      FREE = "FREE"
      PAID = "PAID"
       
      COURSE_CHOICES =[
           ('FREE','free'),
            ('PAID','paid'),
      ]
      STATUS = [
          ('DRAFT','draft'),
          ('PUBLISHED','published'),
          ('ARCHIVED','archived'),
      ]
     
      tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
      title = models.CharField(max_length=255)
      description = models.TextField()    
      course_type = models.CharField(max_length=10, choices=COURSE_CHOICES, default='FREE')
      status = models.CharField(max_length=10, choices=STATUS, default='DRAFT')
      price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
      created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
      skills = models.CharField(max_length=100, default = "IT")

      def __str__(self):
          return self.title
      
class Module(models.Model):
      course = models.ForeignKey(
          Course_db,
          on_delete=models.CASCADE,
          related_name='modules'
     )
      title = models.CharField(max_length=255)
      description = models.TextField()
      order = models.PositiveIntegerField()
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)

      class Meta:
           ordering =['order']
           unique_together = ('course', 'order')
                
      def __str__(self):
          return f"{self.course.title} - {self.title}"
      

class SubModule(models.Model):
     SUBMODULE_TYPE = [
          ('VIDEO','video'),
          ('ASSIGNMENT','assignment')
     ]

     module = models.ForeignKey(
          Module,
          on_delete = models.CASCADE, 
          related_name='submodules'
     )
     title = models.CharField(max_length=255)
     submodule_type = models.CharField(max_length=20, choices=SUBMODULE_TYPE)
     orders = models.PositiveIntegerField()
     video_url = models.URLField(max_length=500, null=True, blank=True)
     assignment_description = models.TextField(null=True, blank=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     class Meta:
          ordering = ['orders']
          unique_together = ('module','orders')

     def __str__(self):
          return f"{self.module.title} - {self.title}"
     
class VideoProgress(models.Model):
     user = models.ForeignKey(
          User,
          on_delete=models.CASCADE,
          related_name="user_videoprogress"
     )
     submodule = models.ForeignKey(
          SubModule,
          on_delete=models.CASCADE,
          related_name="submodule_videoprogress"
     )
     last_duration = models.PositiveIntegerField(default=0)
     video_duration = models.PositiveIntegerField(default=0)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     class Meta:
          unique_together = ("user","submodule")