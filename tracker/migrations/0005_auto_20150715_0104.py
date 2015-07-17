# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracker', '0004_series_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteSites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_url', models.URLField(verbose_name=b'website url')),
                ('submitted_user', models.ForeignKey(default=django.contrib.auth.models.User, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Favorite Sites',
            },
        ),
        migrations.AddField(
            model_name='series',
            name='season',
            field=models.IntegerField(default=1, help_text=b'Season currently on.', blank=True),
        ),
        migrations.AddField(
            model_name='series',
            name='time',
            field=models.TimeField(default=datetime.time(0, 0), help_text=b'Time when the show airs', blank=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='description',
            field=models.TextField(default=b'No description provided.', help_text=b'Optional: Description of the series', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='tag',
            field=models.CharField(default=b'anime', help_text=b'Relevent tag for the series, e.g., anime. Helps with generating a cover image.', max_length=30),
        ),
    ]
