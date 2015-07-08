# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('slug', models.SlugField(unique=True)),
                ('github_url', models.URLField(default=b'https://github.com')),
                ('lang_type', models.CharField(max_length=50)),
                ('site_url', models.URLField(blank=True)),
            ],
        ),
    ]
