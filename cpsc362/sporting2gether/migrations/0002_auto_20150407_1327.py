# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sporting2gether', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='participation',
            unique_together=set([('event', 'user')]),
        ),
    ]
