# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sporting2gether', '0004_auto_20150417_1113'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='participation',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='participation',
            name='event',
        ),
        migrations.RemoveField(
            model_name='participation',
            name='user',
        ),
        migrations.DeleteModel(
            name='Participation',
        ),
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(related_name='event_players', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='creator',
            field=models.ForeignKey(related_name='event_creator', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
