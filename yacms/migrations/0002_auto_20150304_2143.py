# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yacms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmspagetypes',
            name='view_template',
            field=models.CharField(default=None, max_length=32),
            preserve_default=True,
        ),
    ]
