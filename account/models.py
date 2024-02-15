from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from .manager import  UserManager
import uuid
from .manager import UserType
# Create your models here.

    
# Custome  User Model 
class User(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name='Email', max_length=200, unique=True)
    username = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default = False)          #Administrator user
    is_staff = models.BooleanField(default=False)
    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.Jobseeker)
    
    # extra_fiels
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    # def save(self, *args, **kwargs):
    #     """
    #     Only the administrator can create new users.
    #     """
    #     if not self.pk and not self.is_admin:
    #         raise PermissionDenied("Only the administrator can create new users.")
    #     super().save(*args, **kwargs)
    

    
# class  Employer(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.OneToOneField(CustomUser,on_delete=models.CASCADE ,related_name="Employer")
#     company_logo = models.ImageField(upload_to='companylogos/')
#     company_name = models.CharField(max_length=150)
#     website = models.URLField(null=True, blank=True)

# class Jobseeker(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.OneToOneField(CustomUser,on_delete=models.CASCADE , related_name="jobseker")
#     Profile_pic = models.ImageField(upload_to='profilepics/')