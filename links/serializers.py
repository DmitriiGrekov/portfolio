from rest_framework import serializers
from .models import Link


class LinkSerializer(serializers.ModelSerializer):
    """Сериализатор ссылок"""

    class Meta:
        model = Link
        fields = ('pk',
                  'source',
                  'link',
                  )
