from django.urls import path
from .views import (RegistrationAPIView,
                    LoginAPIView,
                    UserRetrieveUpdateAPIView,
                    UserProfileAPIVIew,
                    )
from .views import send_message_user_email
from rest_framework_swagger.views import get_swagger_view


urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('', UserRetrieveUpdateAPIView.as_view(), name='retrieve_update'),
    path('profile/<str:username>/',
         UserProfileAPIVIew.as_view(),
         name='user_profile'),
    path('send_message_email/<int:id>/',
         send_message_user_email,
         name='send_message_user_email')
    ]
