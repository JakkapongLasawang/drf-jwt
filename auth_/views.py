from django.db.utils import IntegrityError

from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import permission_classes

from auth_.serializer import CreateUserSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@permission_classes((permissions.AllowAny,))
class User_(APIView):
    def post(self, request):
        payload = request.data
        serializer = CreateUserSerializer(data=payload)
        if serializer.is_valid():

            try:
                User.objects.create_user(
                    payload["username"], payload["email"], payload["password"]
                )
            except IntegrityError as error:
                return Response({"error": str(error)})
            return Response({"is_success": True})
        return Response(serializer.errors)
