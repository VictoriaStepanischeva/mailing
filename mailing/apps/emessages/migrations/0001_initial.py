# Generated by Django 3.0 on 2020-03-25 14:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Emessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('text_message', models.TextField(blank=True, max_length=1024, null=True, verbose_name='Text message')),
                ('chunk_id', models.IntegerField(verbose_name='Chunk number')),
                ('has_read', models.BooleanField(default=False, verbose_name='Read')),
                ('created_ts', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
            ],
        ),
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('emessage', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='emessages.Emessage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='emessage',
            name='recipients',
            field=models.ManyToManyField(through='emessages.Recipient', to=settings.AUTH_USER_MODEL, verbose_name='Recipients'),
        ),
        migrations.AddField(
            model_name='emessage',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sended_emessages', to=settings.AUTH_USER_MODEL, verbose_name='Sender'),
        ),
    ]
