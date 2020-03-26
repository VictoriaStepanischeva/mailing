from django.contrib import admin

from mailing.apps.emessages.models import Emessage, Recipient


class RecipientInline(admin.TabularInline):
    """Inline for recipient model."""
    model = Recipient
    extra = 2


@admin.register(Emessage)
class MessageAdmin(admin.ModelAdmin):
    """Admin for Emessage."""

    list_display = ('sender', 'has_read', 'is_deleted')
    list_filter = ('has_read', 'is_deleted')
    raw_id_fields = ('sender', 'recipients')
    inlines = (RecipientInline, )
