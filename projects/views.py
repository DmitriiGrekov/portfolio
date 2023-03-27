from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProjectSerializer
from users.auth import JWTAuthentication
from .models import Project, Link
from users.models import Skill
from .dto import (SkillType,
                  LinkType,
                  SkillLinkType)
from .renderers import ResponseJSONRenderer


class ProjectAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ProjectSerializer
    renderer_classes = (ResponseJSONRenderer,)

    def get(self, request, username):
        """Получение проектов пользователя по id пользователя"""
        try:
            projects = Project.objects.filter(user__username=username)
            serializer = self.serializer_class(projects, many=True)
            return Response({'data': serializer.data},
                            status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'status': 404, 'message': 'Not Found'},
                            status=status.HTTP_404_NOT_FOUND)


class ProjectCreateAPIView(APIView):
    """Создание проектов"""
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer
    renderer_classes = (ResponseJSONRenderer,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
        """Создание проекта"""
        project = request.data

        links_and_skills = _get_links_and_skills_from_request(request)

        serializer = self.serializer_class(data=project)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user,
                        skills=links_and_skills.skills_data.skills,
                        links=links_and_skills.links_data.links)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectUpdateDeleteAPIView(APIView):
    """Обновление и удаление проектов"""
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer
    renderer_classes = (ResponseJSONRenderer,)
    authentication_classes = (JWTAuthentication,)

    def patch(self, request, project_id):
        """Обновление проекта"""
        try:
            project = Project.objects.get(pk=project_id,
                                          user__id=request.user.pk)
            data = request.data
            links_and_skills = _get_links_and_skills_from_request(request,
                                                                  project)
            serializer = self.serializer_class(project,
                                               data=data,
                                               partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(skills=links_and_skills.skills_data.skills,
                            links=links_and_skills.links_data.links)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'status': 404, 'message': 'Not Found'},
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, project_id):
        """Удаление проекта пользователем"""
        try:
            project = Project.objects.get(pk=project_id,
                                          user__id=request.user.pk)
            project.delete()
            return Response({'status': 204, 'message': 'Successfully delete'},
                            status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({'status': 404, 'message': 'Not Found'},
                            status=status.HTTP_404_NOT_FOUND)


def _get_links_from_request(request, project=None) -> LinkType:
    """Получаем ссылки из запроса"""
    links_data = request.data.get('links')
    if links_data:
        links = Link.objects.filter(
                id__in=list(map(int,
                                links_data.split(', '))))
    else:
        if project:
            links = project.links.all()
        else:
            links = []
    return LinkType(links=links)


def _get_skills_from_request(request, project=None) -> SkillType:
    """Получаем скиллы из запроса"""
    skills_data = request.data.get('skills')
    if skills_data:
        skills = Skill.objects.filter(
                id__in=list(map(int,
                                skills_data.split(', '))))
    else:
        if project:
            skills = project.skills.all()
        else:
            skills = []
    return SkillType(skills=skills)


def _get_links_and_skills_from_request(request, project=None) -> SkillLinkType:
    """Вытаскиваем из request ссылки и скилы"""
    links = _get_links_from_request(request, project)
    skills = _get_skills_from_request(request, project)
    return SkillLinkType(links_data=links, skills_data=skills)
