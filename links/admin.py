from django.contrib import admin
from .models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'link',)
    list_display_links = ('source', 'link',)
