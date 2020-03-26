from mailing.apps.emessages.models import Emessage

class SetUpEmessageMixin(object):
    """Mixin for emessage settings."""

    def _create_emessage(self, sender, **kwargs):
        return Emessage.objects.create(sender=sender, **kwargs)
