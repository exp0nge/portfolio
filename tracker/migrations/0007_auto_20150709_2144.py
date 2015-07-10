# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_auto_20150709_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='stream_site',
            field=models.URLField(help_text=b'URL to view this series.', blank=True),
        ),
    ]
