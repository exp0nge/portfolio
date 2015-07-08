# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'The title of the series.', max_length=200)),
                ('description', models.TextField(default=b'No description provided.', help_text=b'Optional: Description of the series', max_length=500, blank=True)),
                ('release_day', models.CharField(help_text=b'Release day, e.g., Monday', max_length=10, choices=[(b'MONDAY', b'Monday'), (b'TUEDAY', b'Tuesday'), (b'WEDNESDAY', b'Wednesday'), (b'THURSDAY', b'Thursday'), (b'FRIDAY', b'Friday'), (b'SATURDAY', b'Saturday'), (b'SUNDAY', b'Sunday'), (b'UNKNOWN', b'Unknown')])),
                ('stream_site', models.URLField(help_text=b'URL to view this series.', blank=True)),
                ('cover_image_url', models.URLField(help_text=b'Cover image URL.', blank=True)),
                ('submitted_user', models.ForeignKey(default=django.contrib.auth.models.User, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'series',
            },
        ),
    ]
