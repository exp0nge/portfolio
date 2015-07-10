# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_series_current_episode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='release_day',
            field=models.CharField(help_text=b'Release day, e.g., Monday', max_length=10, choices=[(b'MONDAY', b'Monday'), (b'TUESDAY', b'Tuesday'), (b'WEDNESDAY', b'Wednesday'), (b'THURSDAY', b'Thursday'), (b'FRIDAY', b'Friday'), (b'SATURDAY', b'Saturday'), (b'SUNDAY', b'Sunday'), (b'UNKNOWN', b'Unknown')]),
        ),
    ]
