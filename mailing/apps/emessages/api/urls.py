from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from mailing.apps.emessages.api.views import (
    EmessageCreateView,
    InboxEmessagesViewSet,
    SentEmessagesViewSet
)

urlpatterns = [
    url(r'^create/', EmessageCreateView.as_view(), name='emessage-create'),
]

router = DefaultRouter()
router.register('inbox', InboxEmessagesViewSet, 'inbox')
router.register('sent', SentEmessagesViewSet, 'sent')
urlpatterns += router.urls