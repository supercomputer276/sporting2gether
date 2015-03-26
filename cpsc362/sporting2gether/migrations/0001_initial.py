# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('start_datetime', models.DateTimeField(verbose_name=b'Date & Time')),
                ('capacity', models.PositiveIntegerField()),
                ('category', models.CharField(max_length=4, verbose_name=b'Sport', choices=[(b'BASE', b'Baseball'), (b'BASK', b'Basketball'), (b'VOLL', b'Volleyball'), (b'SOCC', b'Soccer / Football'), (b'FOOT', b'American Football'), (b'GOLF', b'Golf'), (b'TENN', b'Tennis'), (b'SWIM', b'Swimming'), (b'SKII', b'Skiing'), (b'SNOW', b'Snowboarding'), (b'OTHR', b'Other')])),
                ('location_main', models.CharField(max_length=50)),
                ('location_city', models.CharField(max_length=25)),
                ('location_zip', models.CharField(max_length=5)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(to='sporting2gether.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_no', models.CharField(max_length=10, verbose_name=b'Phone # (digits)')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='participation',
            name='user',
            field=models.ForeignKey(to='sporting2gether.Users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='creator',
            field=models.ForeignKey(to='sporting2gether.Users'),
            preserve_default=True,
        ),
    ]
