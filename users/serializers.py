from rest_framework import serializers
from django.contrib.auth import authenticate
from skills.serializers import SkillSerializer
from facts.serializers import FactSerializer
from projects.serializers import ProjectSerializer
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import User
from PIL import Image
from rembg import remove
from io import BytesIO
import uuid


class RegistrationSerializer(serializers.ModelSerializer):
    """Регистрация пользователя"""
    password = serializers.CharField(
            max_length=128,
            min_length=8,
            write_only=True
            )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Авторизация пользователя"""
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """Аутентификация пользователя"""
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('An email address is required to log in')

        if password is None:
            raise serializers.ValidationError('An password address is required to log in')

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        return {
                'email': user.email,
                'username': user.get_username(),
                'token': user.token
                }


class UserSerializer(serializers.ModelSerializer):
    """Обновление и вывод пользователя"""
    skills = SkillSerializer(read_only=True, many=True)
    delete_background = serializers.BooleanField(default=False)
    facts = FactSerializer(read_only=True, many=True)
    projects = ProjectSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('email',
                  'username',
                  'about',
                  'discord',
                  'first_name',
                  'last_name',
                  'image',
                  'skills',
                  'delete_background',
                  'facts',
                  'projects',
                  )
        read_only_fields = ('token',)

    def _delete_background(self, imageField: serializers.ImageField,
                           size: tuple):
        """Удаляем задний фон на фото"""
        im = Image.open(imageField)
        im = remove(im)
        output = BytesIO()
        im.save(output, format='PNG')
        random_name = f'{uuid.uuid4()}.png'
        temp_file = InMemoryUploadedFile(output,
                                         None,
                                         random_name,
                                         'image/png',
                                         len(output.getbuffer()), None)
        return temp_file

    def update(self, instance, validated_data):
        """Обновляем данные пользователя"""
        password = validated_data.pop('password', None)
        delete_background = validated_data.pop('delete_background', None)

        if delete_background:
            instance.image = self._delete_background(
                    validated_data.pop('image', None), (50, 50)
                    )

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
