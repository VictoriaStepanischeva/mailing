from django.contrib.auth.hashers import make_password
from mailing.apps.users.models import User

class SetUpUserMixin(object):
    """Mixin for user settings."""

    def _create_user(self, email, password, **kwargs):
        return User.objects.create(email=email, password=password, **kwargs)