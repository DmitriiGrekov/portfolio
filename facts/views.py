from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from projects.renderers import ResponseJSONRenderer
from rest_framework.response import Response
from rest_framework import status

from users.auth import JWTAuthentication
from .serializers import FactSerializer


class FactAPIView(APIView):
    renderer_classes = (ResponseJSONRenderer,)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = FactSerializer

    def post(self, request):
        """Создание фактов"""
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
