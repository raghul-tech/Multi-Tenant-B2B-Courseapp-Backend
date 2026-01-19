from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from tenant.models import Tenant

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role='TENANT_USER', **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)  
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(email, password, role='SUPER_ADMIN', **extra_fields)
        return user



class User(AbstractBaseUser, PermissionsMixin):

    SUPER_ADMIN = "SUPER_ADMIN"
    TENANT_ADMIN = "TENANT_ADMIN"
    TENANT_USER = "TENANT_USER"

    ROLE_CHOICES = (
        ('SUPER_ADMIN', 'Super Admin'),
        ('TENANT_ADMIN', 'Tenant Admin'),
        ('TENANT_USER', 'Tenant User'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email






