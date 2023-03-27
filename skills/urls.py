from django.urls import path
from .views import SkillAPIVIew, SkillDetailAPIView


urlpatterns = [
        path('', SkillAPIVIew.as_view(), name='skill_list'),
        path('<int:skill_id>/',
             SkillDetailAPIView.as_view(),
             name='skill_detail'),
        ]
