from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils import timezone



# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
            Creates, saves and return a User with the given email, username, and password.
        """

        if not email:
            raise ValueError('user must have a email address')
        if not first_name:
            raise ValueError('first name is required')
        if not last_name:
            raise ValueError('last name is required')
        
        user = self.model(first_name=first_name, last_name=last_name, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, first_name, last_name, password=None):
        """
            Creates, saves, and returns a superuser with the given email, username, and password.
        """
        if password is None:
            raise ValueError('password should not be none')
        user=self.create_user(email,first_name,last_name,password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save()
        return user




AUTH_PROVIDERS={'email':'email', 'google':'google'}
# Custom User model with email as the unique identifier
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255,null=True, blank=True)
    last_name = models.CharField(max_length=255,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified= models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    auth_provider = models.CharField(max_length=50, blank=False,null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"
    
    @property
    def get_full_name(self):
        return f"{self.first_name} - {self.last_name}"
    
    def tokens(self):
        pass


class  OneTimePassword(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name}-passcode"

