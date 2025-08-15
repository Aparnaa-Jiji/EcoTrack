from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid

# ------------------------
# Custom user manager
# Handles user creation and superuser creation
# ------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a normal user with an email and password.
        Raises ValueError if email is not provided.
        """
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)  # Normalize email domain part
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash the password properly
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with all required permissions.
        Ensures is_staff, is_superuser, and is_active flags are True.
        Sets the role as 'admin'.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Superusers must be active
        extra_fields.setdefault('role', 'admin')    # Explicitly assign admin role

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


# ------------------------
# Custom user model
# Extends AbstractBaseUser and PermissionsMixin for Django auth integration
# ------------------------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Define role choices for role-based access control
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('collector', 'Collector'),
        ('citizen', 'Citizen'),
    )

    # Email field used as the unique identifier for authentication
    email = models.EmailField(unique=True)

    # Additional user details
    name = models.CharField(max_length=100)
    

    
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    # Role assigned to user
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')

    # Status fields
    is_active = models.BooleanField(default=True)   # Whether the user is active (can log in)
    is_staff = models.BooleanField(default=False)   # Whether the user can access admin site

    # Permissions related ManyToMany fields
    # Customized related_name to avoid clashes with default User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True
    )

    # Email is used as the username field for authentication
    USERNAME_FIELD = 'email'

    # Required fields for creating a superuser via createsuperuser command
    REQUIRED_FIELDS = ['name']

    # Link the custom manager
    objects = CustomUserManager()

    def __str__(self):
        # Return the email as string representation of user
        return self.email
