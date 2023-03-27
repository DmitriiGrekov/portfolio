from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Проекты"""
    list_display = ('title', 'status', 'user',)
