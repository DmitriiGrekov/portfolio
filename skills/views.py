from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import SkillSerializer
from projects.renderers import ResponseJSONRenderer
from rest_framework.response import Response
from .models import Skill


class SkillAPIVIew(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SkillSerializer
    renderer_classes = (ResponseJSONRenderer,)

    def get(self, request):
        """Получение списка скиллов"""
        projects = Skill.objects.all().order_by('id')
        serializer = self.serializer_class(projects, many=True)
        return Response({'data': serializer.data},
                        status=status.HTTP_200_OK)


class SkillDetailAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SkillSerializer
    renderer_classes = (ResponseJSONRenderer,)

    def get(self, request, skill_id):
        """Получение одного скилла"""
        try:
            skill = Skill.objects.get(pk=skill_id)
            serializer = self.serializer_class(skill)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Skill.DoesNotExist:
            return Response({'status': 404, 'message': 'Not Found'},
                            status=status.HTTP_404_NOT_FOUND)
