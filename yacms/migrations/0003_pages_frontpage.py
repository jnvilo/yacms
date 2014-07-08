# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yacms', '0002_paths_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='pages',
            name='frontpage',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
