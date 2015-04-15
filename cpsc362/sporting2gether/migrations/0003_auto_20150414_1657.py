# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sporting2gether', '0002_auto_20150407_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='phone_no',
            field=models.CharField(max_length=10, verbose_name=b'Phone # (digits)', blank=True),
            preserve_default=True,
        ),
    ]
