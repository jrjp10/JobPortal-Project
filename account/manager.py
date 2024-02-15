from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db import models

class UserType(models.TextChoices):
    Jobseeker = 'JOBSEEKER', ('Jobseeker')
    Employer = 'EMPLOYER', ('Employer')
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, user_type=UserType.Jobseeker, **extra_fields):
        """
        Create and save a user with the given email, username and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),  # Normalize the address
            username=username,
            user_type=user_type,
            **extra_fields,
        )
        user.set_password(password)   # Hash the password before saving it in the database
        user.save(using=self._db)     # Using the correct database alias to ensure
        return user                   # that this is the one where the new user will be created
    
    def create_superuser(self, email, username, password=None, **extra_field):
        extra_field.setdefault('is_staff',True)
        extra_field.setdefault('is_superuser',True)
        extra_field.setdefault('is_active',True)

        if extra_field.get('is_staff') is not True:
            raise ValueError(
                'super user must assigned to is_staff=True')
        
        if extra_field.get('is_superuser') is not True:
            raise ValueError(
                'Superuser Must be assigned to is_superuser=True')
        
        return self.create_user(email,username,password,**extra_field)
        

