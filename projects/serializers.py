from rest_framework import serializers
from .models import Project
from skills.serializers import SkillSerializer
from links.serializers import LinkSerializer


class ProjectSerializer(serializers.ModelSerializer):
    """Сериализатор проектов"""
    skills = SkillSerializer(read_only=True, many=True)
    links = LinkSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = ('pk',
                  'title',
                  'short_description',
                  'description',
                  'image',
                  'links',
                  'skills',
                  'status',
                  'created_at',
                  )

    def create(self, validated_data):
        """Создание проекта пользователя"""
        links = validated_data.pop('links')
        skills = validated_data.pop('skills')
        project = Project.objects.create(**validated_data)
        project.links.add(*links)
        project.skills.add(*skills)
        return project

    # def update(self, instance, validated_data):
    #     """Обновление проекта пользователя"""
