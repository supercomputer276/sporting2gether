# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sporting2gether', '0006_auto_20150423_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_datetime',
            field=models.DateTimeField(null=True, verbose_name=b'Ending Date & Time', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='start_datetime',
            field=models.DateTimeField(verbose_name=b'Staring Date & Time'),
            preserve_default=True,
        ),
    ]
