import uuid
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mailing.apps.users.models import User
from mailing.apps.users.api.serializers import UserSerializer

class RegisterUserView(generics.CreateAPIView):
    """API for user registration."""

    model = User
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Override to make new user active."""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class LogoutUserView(views.APIView):
    """API for user logout."""

    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        """Override to replace jwt_secret."""
        user = request.user
        user.jwt_secret = uuid.uuid4()
        user.save()
        return Response(status=status.HTTP_200_OK)





