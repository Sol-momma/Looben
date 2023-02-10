# Generated by Django 4.0.6 on 2022-11-30 04:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_rename_seen_messages_is_seen'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConversationPartner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conversation_partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversation_partner', to=settings.AUTH_USER_MODEL, verbose_name='受信者')),
                ('current_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_user', to=settings.AUTH_USER_MODEL, verbose_name='送信者')),
            ],
            options={
                'verbose_name_plural': 'チャットユーザーリスト',
            },
        ),
    ]
