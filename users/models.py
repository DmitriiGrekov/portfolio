from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from datetime import datetime, timedelta
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files import File
from skills.models import Skill
from PIL import Image

import jwt


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password')
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser, PermissionsMixin):
    """Модель кастомного пользователя"""
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    about = models.TextField(null=True, blank=True, verbose_name='О себе')
    discord = models.CharField(max_length=300,
                               blank=True,
                               null=True,
                               verbose_name='Дискорд')
    is_active = models.BooleanField(default=True,
                                    verbose_name='Пользователь активен')
    is_staff = models.BooleanField(default=False,
                                   verbose_name='Доступ к админ панели')
    skills = models.ManyToManyField(Skill, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image = models.ImageField(verbose_name='Изображение пользователя',
                              blank=True,
                              null=True
                              )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} -> {self.email}'

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=365)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
            }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
