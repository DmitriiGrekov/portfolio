from django.urls import path
from .views import FactAPIView


urlpatterns = [
        path('', FactAPIView.as_view(), name='create_fact'),
        ]
