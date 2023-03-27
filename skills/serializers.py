from rest_framework import serializers
from .models import Skill


class SkillSerializer(serializers.ModelSerializer):
    """Сериализатор скиллов"""

    class Meta:
        model = Skill
        fields = '__all__'
