from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class Template(models.Model):
    name = models.CharField(max_length=100)
    hash = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'templates'


class Domain(models.Model):
    id_template = models.ForeignKey(Template, on_delete=models.CASCADE, db_column='id_template')
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='id_user')
    name = models.CharField(max_length=255)
    uuid = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'domains'


class CustomUserManager(BaseUserManager):
    """Custom user manager where email is the unique identifiers."""

    def create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('L\'adresse email doit être définie')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Le superutilisateur doit avoir is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Le superutilisateur doit avoir is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model where email is the unique identifier."""
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
