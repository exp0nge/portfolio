# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_auto_20150715_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritesites',
            name='site_url',
            field=models.URLField(default=b''),
        ),
    ]
