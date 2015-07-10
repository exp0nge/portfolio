# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_series_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='tag',
            field=models.CharField(default=b'anime', help_text=b'Relevent tag for the series, e.g., anime. Helps with generating a cover image.', max_length=30),
        ),
    ]
