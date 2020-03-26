from django.db import models
from mailing.apps.users.models import User


class Emessage(models.Model):
    """Electronic message model."""

    sender = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='sended_emessages',
        verbose_name='Sender'
    )
    recipients = models.ManyToManyField(
        User,
        verbose_name='Recipients',
        through='Recipient'
    )
    is_deleted = models.BooleanField(default=False)
    text_message = models.TextField(
        'Text message', max_length=1024, blank=True, null=True)
    chunk_id = models.IntegerField('Chunk number', default=1)
    has_read = models.BooleanField('Read', default=False)
    created_ts = models.DateTimeField('Creation date', auto_now_add=True)


class Recipient(models.Model):
    """Recipient model."""

    emessage = models.ForeignKey(Emessage, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_deleted = models.BooleanField(default=False)

