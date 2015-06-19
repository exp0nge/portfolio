# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myportfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='lang_type',
            field=models.CharField(default='Java', max_length=50),
            preserve_default=False,
        ),
    ]
