from rest_framework import serializers
from .models import Fact


class FactSerializer(serializers.ModelSerializer):
    """Сериализация фактов"""

    class Meta:
        model = Fact
        fields = ('text', )
