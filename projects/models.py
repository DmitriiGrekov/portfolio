from django.db import models
from skills.models import Skill
from users.models import User
from links.models import Link


class Project(models.Model):
    """Проекты"""
    PROJECT_STATUS = (
            ('complete', 'Завершенные приложения'),
            ('small', 'Маленькие проекты')
            )

    title = models.CharField(max_length=100,
                             verbose_name='Название проекта')
    short_description = models.CharField(max_length=255,
                                         verbose_name='Короткое описание проекта',
                                         blank=True,
                                         null=True)
    description = models.TextField(verbose_name='Описание',
                                   blank=True,
                                   null=True)
    image = models.ImageField('Изображение проекта')
    links = models.ManyToManyField(Link, related_name='projects')
    skills = models.ManyToManyField(Skill, related_name='projects')
    status = models.CharField(max_length=255,
                              choices=PROJECT_STATUS,
                              verbose_name='Статус проекта')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='projects')

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата обновления')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
