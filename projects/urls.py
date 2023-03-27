from django.urls import path
from .views import (ProjectAPIView,
                    ProjectCreateAPIView,
                    ProjectUpdateDeleteAPIView)


urlpatterns = [
        path('<int:project_id>/',
             ProjectUpdateDeleteAPIView.as_view(),
             name='project_update_delete'
             ),
        path('user/<str:username>/', ProjectAPIView.as_view(),
             name='project_user_list'),
        path('user/',
             ProjectCreateAPIView.as_view(),
             name='project_created'),
        ]
