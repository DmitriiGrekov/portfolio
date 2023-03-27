# Generated by Django 4.1.7 on 2023-03-23 04:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('skills', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название ссылки')),
                ('link', models.TextField(verbose_name='Ссылка')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название проекта')),
                ('short_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Короткое описание проекта')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение проекта')),
                ('status', models.CharField(choices=[('complete', 'Завершенные приложения'), ('small', 'Маленькие проекты')], max_length=255, verbose_name='Статус проекта')),
                ('links', models.ManyToManyField(related_name='projects', to='projects.link')),
                ('skills', models.ManyToManyField(related_name='projects', to='skills.skill')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
            },
        ),
    ]