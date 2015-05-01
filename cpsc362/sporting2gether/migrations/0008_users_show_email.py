# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sporting2gether', '0007_auto_20150430_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='show_email',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
