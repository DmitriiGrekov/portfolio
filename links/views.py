from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from projects.renderers import ResponseJSONRenderer
from .serializers import LinkSerializer
from users.auth import JWTAuthentication


class LinksAPIView(APIView):
    renderer_classes = (ResponseJSONRenderer,)
    serializer_class = LinkSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Создание ссылок для проектов"""
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
