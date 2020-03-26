import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


def jwt_get_secret_key(user_model):
    return user_model.jwt_secret


class UserManager(BaseUserManager):
    """Manager for user objects."""

    def create_user(self, email, password=None):
        """Create and return a `User` with email and password."""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and return a `User` with superuser (admin) permissions."""
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.is_confirmed = True
        user.save()

        return user


class User(AbstractBaseUser):
    """Custom user model."""

    email = models.EmailField('Email address', max_length=255, unique=True)
    name = models.CharField(max_length=128, blank=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    jwt_secret = models.UUIDField(default=uuid.uuid4)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission."""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app."""
        return True