from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .auth import JWTAuthentication
from .serializers import (RegistrationSerializer,
                          LoginSerializer,
                          UserSerializer
                          )
from .renderers import UserJSONRenderer
from .models import User


class RegistrationAPIView(APIView):
    """Регистрация пользователя"""
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """Авторизация пользователя"""
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """Просмотр и обновление пользователя"""
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)

    def retrieve(self, request, *args, **kwargs):
        """Получение авторизованного пользователя"""
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """Обнолвение пользователя"""
        serialzier_data = request.data
        serializer = self.serializer_class(
                request.user,
                data=serialzier_data,
                partial=True
                )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileAPIVIew(APIView):
    """Получение профиля пользователя"""
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def get(self, request,  username):
        """Получеие профиля пользователя"""
        try:
            user = User.objects.get(username=username)
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'status': 404, 'message': 'Not Found'},
                            status=status.HTTP_404_NOT_FOUND)


def send_message_user_email(request, id):
    """Отправка сообщений пользователю из админ панели"""
    if request.method == 'POST':
        try:
            user = User.objects.get(pk=id)
            message = request.POST.get('message')
            send_mail('Сообщение из админ панели DJANGO',
                      message,
                      settings.EMAIL_HOST_USER,
                      [user.email])
            messages.info(request, 'Сообщение успешно отправлено')
            return HttpResponseRedirect(
                    reverse('admin:users_user_change', args=[id]))
        except:
            messages.error(request, 'Ошибка отправки')
            return HttpResponseRedirect(
                    reverse('admin:users_user_change', args=[id]))
    return HttpResponseRedirect(request.get_full_path())
