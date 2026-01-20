from django.db import models

# Create your models here.
class Skills(models.Model):
    skill = models.CharField(max_length=225)
    
