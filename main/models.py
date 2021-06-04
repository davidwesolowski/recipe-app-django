import uuid
from django.db import models
from django_enumfield import enum
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class Roles(enum.Enum):
    ADMIN = 0
    USER = 1

    __labels__ = {
        ADMIN: 'ADMINISTRATOR',
        USER: 'UŻYTKOWNIK'
    }


class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('rola', Roles.ADMIN)
        return self.create_user(email, name, password, **other_fields)

    def create_user(self, email, name, password, **other_fields):
        if not email:
            raise ValueError('Adres email jest wymagany')

        email = self.normalize_email(email)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('rola', Roles.USER)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    ID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField('Nazwa', max_length=200)
    email = models.EmailField('Adres email', unique=True)
    rola = enum.EnumField(Roles)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class Recipes(models.Model):
    ID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    userID = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    imageUrl = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Recipes'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.title + ' ' + str(self.ID)
