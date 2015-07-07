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
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'The title of the series.', max_length=200)),
                ('description', models.TextField(help_text=b'Optional: Description of the series', max_length=500, blank=True)),
                ('release_day', models.CharField(help_text=b'Release day, e.g., Monday', max_length=10, choices=[(b'MONDAY', b'Monday'), (b'TUEDAY', b'Tuesday'), (b'WEDNESDAY', b'Wednesday'), (b'THURSDAY', b'Thursday'), (b'FRIDAY', b'Friday'), (b'SATURDAY', b'Saturday'), (b'SUNDAY', b'Sunday'), (b'UNKNOWN', b'Unknown')])),
                ('stream_site', models.URLField(help_text=b'URL to view this series.', blank=True)),
                ('cover_image', models.ImageField(upload_to=b'series_imgs', blank=True)),
            ],
            options={
                'verbose_name_plural': 'series',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='series',
            name='sumbmitted_user',
            field=models.ForeignKey(to='tracker.UserProfile'),
            preserve_default=True,
        ),
    ]
