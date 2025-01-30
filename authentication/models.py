import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number, password, **extra_fields):
        """
        Create and return a user with an email and password.
        """
        if not mobile_number:
            raise ValueError('The Mobile number must be set')
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password, **extra_fields):
        """
        Create and return a superuser with mobile number, password, and admin rights.
        """
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(mobile_number, password, **extra_fields)


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False)
    age = models.PositiveIntegerField(null=False)
    gender = models.CharField(max_length=10, null=False, blank=False)
    mobile_number = models.CharField(max_length=15, null=False, unique=True)
    photo_url = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # For soft delete or deactivation
    is_staff = models.BooleanField(default=False)  # For admin access control
    is_superuser = models.BooleanField(default=False)  # For superuser control
    created_at = models.DateTimeField(auto_now_add=True)

    # Add any other custom fields for your application here.

    objects = CustomUserManager()  # Attach the custom manager to the model

    USERNAME_FIELD = 'mobile_number'  # The field used for login (must be unique)
    REQUIRED_FIELDS = ['name', 'age', 'gender']  # Fields required for creating a user

    def __str__(self):
        return self.name

    @property
    def is_authenticated(self):
        # Return True if the user is authenticated; you can add your verification logic here.
        return self.is_verified

