# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_auto_20150709_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='stream_site',
            field=models.URLField(default=b'http://', help_text=b'URL to view this series.', blank=True),
        ),
    ]
