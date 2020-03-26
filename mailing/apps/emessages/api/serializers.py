from django.core.exceptions import ValidationError
from rest_framework import serializers

from mailing.apps.users.models import User
from mailing.apps.emessages.models import Emessage

class EmessageSerializer(serializers.ModelSerializer):
    """Electronic message serializer."""

    sender = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=User.objects.get_queryset()
    )
    recipients = serializers.PrimaryKeyRelatedField(
        required=True,
        many=True,
        queryset=User.objects.get_queryset()
    )

    def validate(self, attrs):
        """Override to not allow empty recipients."""
        super(EmessageSerializer, self).validate(attrs)
        recipients = attrs.get('recipients')
        if not recipients:
            raise ValidationError(
                {'recipients': 'Recipients field cannot be empty'}
            )
        return attrs

    class Meta:
        model = Emessage
        fields = ('id', 'sender', 'recipients', 'text_message',
                  'has_read')