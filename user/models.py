from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils import timezone



# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
            Creates, saves and return a User with the given email, username, and password.
        """

        if not email:
            raise ValueError('user must have a email address')
        if not username:
            raise ValueError('user must have a username')
        
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, username, password=None):
        """
            Creates, saves, and returns a superuser with the given email, username, and password.
        """
        if password is None:
            raise ValueError('password should not be none')
        user=self.create_user(email,username,password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

# Custom User model with email as the unique identifier
class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f"{self.username}"
