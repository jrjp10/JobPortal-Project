from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from .manager import  UserManager
import uuid

# Create your models here.
    
# Custome  User Model 
class User(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name='Email', max_length=200, unique=True)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=128)
    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default = False)          #Administrator user
    is_staff = models.BooleanField(default=False)
    is_jobseeker = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)

    
    # extra_fiels
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    # def save(self, *args, **kwargs):
    #     """
    #     Only the administrator can create new users.
    #     """
    #     if not self.pk and not self.is_admin:
    #         raise PermissionDenied("Only the administrator can create new users.")
    #     super().save(*args, **kwargs)
    

    