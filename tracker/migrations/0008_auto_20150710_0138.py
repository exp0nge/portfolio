# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_auto_20150709_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='description',
            field=models.TextField(default=b'No description provided.', help_text=b'Optional: Description of the series', max_length=200, blank=True),
        ),
    ]
