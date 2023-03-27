# Generated by Django 4.1.7 on 2023-03-24 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(choices=[('live', 'Live'), ('cached', 'Cached'), ('github', 'Github')], max_length=255, verbose_name='Куда ведет ссылка')),
                ('link', models.URLField(verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'Ссылка',
                'verbose_name_plural': 'Ссылки',
            },
        ),
    ]