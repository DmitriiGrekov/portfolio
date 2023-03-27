from django.db import models


class Skill(models.Model):
    """Модель скиллов"""
    SKILL_TYPE = (
            ('languages', 'Языки'),
            ('databases', 'Базы данных'),
            ('tools', 'Инструменты'),
            ('frameworks', 'Фреймворки'),
            ('other', 'Другие'),
            )
    name = models.CharField(max_length=100, verbose_name='Название скилла')
    type = models.CharField(max_length=100,
                            verbose_name='Тип',
                            choices=SKILL_TYPE,
                            default='languages')

    def __str__(self):
        return f'{self.type} -> {self.name}'

    class Meta:
        verbose_name = 'Скилл'
        verbose_name_plural = 'Скиллы'
