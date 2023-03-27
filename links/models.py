from django.db import models


class Link(models.Model):
    """Ссылки на проекты"""
    LINK_STATUS = (
            ('live', 'Live'),
            ('cached', 'Cached'),
            ('github', 'Github')
            )
    source = models.CharField(max_length=255,
                              verbose_name='Куда ведет ссылка',
                              choices=LINK_STATUS)
    link = models.URLField('Ссылка')

    def __str__(self):
        return f'{self.source} -> {self.link}'

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'
