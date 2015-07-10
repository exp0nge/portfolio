# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='current_episode',
            field=models.IntegerField(default=1, help_text=b'Current episode you are on.'),
        ),
    ]
