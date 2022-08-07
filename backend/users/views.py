from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import MyTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        tokens = MyTokenObtainPairSerializer(request.data).validate(
            request.data,
        )
        return Response(tokens, status=status.HTTP_200_OK)
