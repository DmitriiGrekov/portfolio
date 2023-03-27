from django.db import models
from users.models import User


class Fact(models.Model):
    text = models.CharField(max_length=300, verbose_name='Текст факта')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='facts',
                             verbose_name='Пользователь')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Факт'
        verbose_name_plural = 'Факты'
