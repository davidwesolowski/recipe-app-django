from django.db import models
from django_enumfield import enum
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class Roles(enum.Enum):
    ADMIN = 0
    USER = 1

'''
class Users(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=256)
    role = enum.EnumField(Roles)

    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.name + ' ' + str(self.id)
'''


class CustomUserManager(BaseUserManager):

    def create_super_user(self, email, name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('role', Roles.ADMIN)
        return self.create_user(email, name, password, **other_fields)

    def create_user(self, email, name, password, **other_fields):
        if not email:
            raise ValueError('Adres email jest wymagany')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        other_fields.setdefault('role', Roles.USER)
        user.set_password(password)
        user.save()
        return user


class UsersBase(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=200)
    email = models.EmailField('Adres email', unique=True)
    role = enum.EnumField(Roles)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class Recipes(models.Model):
    userId = models.ForeignKey(UsersBase, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2048)
    imageUrl = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.title + ' ' + str(self.id)