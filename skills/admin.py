from django.contrib import admin
from .models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Скиллы"""
    list_display = ('name', 'type',)
