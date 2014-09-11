# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yacms', '0004_auto_20140713_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='pages',
            name='meta_description',
            field=models.TextField(default='', max_length=20480),
            preserve_default=True,
        ),
    ]
