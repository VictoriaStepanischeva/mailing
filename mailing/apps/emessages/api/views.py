from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mailing.apps.emessages.models import Emessage, Recipient
from mailing.apps.emessages.api.serializers import EmessageSerializer


class EmessageCreateView(generics.CreateAPIView):
    """API for creating messages."""

    # TODO: if the message is larger than 1024
    #  then split it into several chunks.
    permission_classes = [IsAuthenticated]
    model = Emessage
    serializer_class = EmessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class InboxEmessagesViewSet(mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """API for user's inbox messages."""

    permission_classes = [IsAuthenticated]
    model = Emessage
    serializer_class = EmessageSerializer

    def get_queryset(self):
        return Emessage.objects.filter(
            recipients=self.request.user,
            recipient__is_deleted=False).order_by('-created_ts')

    def destroy(self, request, *args, **kwargs):
        """Override to set is_deleted status for inbox message."""
        emessage = self.get_object()
        recipient = Recipient.objects.filter(
            emessage=emessage, user=self.request.user).first()
        recipient.is_deleted = True
        recipient.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def read(self, request, pk=None):
        """Marking inbox message as read."""
        emessage = self.get_object()
        emessage.has_read = True
        emessage.save()
        return Response(self.serializer_class(emessage).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def unread(self, request, pk=None):
        """Marking inbox message as unread."""
        emessage = self.get_object()
        emessage.has_read = False
        emessage.save()
        return Response(self.serializer_class(emessage).data,
                        status=status.HTTP_200_OK)


class SentEmessagesViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """API for user's sent messages."""

    permission_classes = [IsAuthenticated]
    model = Emessage
    serializer_class = EmessageSerializer

    def get_queryset(self):
        return Emessage.objects.filter(
            sender=self.request.user, is_deleted=False).order_by('-created_ts')

    def destroy(self, request, *args, **kwargs):
        """Override to set is_deleted status for sent message."""
        emessage = self.get_object()
        emessage.is_deleted = True
        emessage.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
