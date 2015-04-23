# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sporting2gether', '0005_auto_20150417_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_cancelled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='location_city',
            field=models.CharField(max_length=25, verbose_name=b'City'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='location_main',
            field=models.CharField(max_length=50, verbose_name=b'Address'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='location_zip',
            field=models.CharField(max_length=5, verbose_name=b'ZIP Code'),
            preserve_default=True,
        ),
    ]
