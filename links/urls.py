from django.urls import path
from .views import LinksAPIView


urlpatterns = [
        path('', LinksAPIView.as_view(), name='links_create'),
        ]
