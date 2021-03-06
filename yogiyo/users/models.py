from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='profile')
    point = models.PositiveIntegerField(null=True, blank=True)
    nickname = models.CharField(max_length=20, null=True, blank=True)
    phone_num = PhoneNumberField(null=True, blank=True)


class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.id:
            self.set_password(self.password)
        super().save(*args, **kwargs)


class Bookmark(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='bookmark')
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='bookmark')

    class Meta:
        unique_together = ['user', 'restaurant']
