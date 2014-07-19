# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('yacms', '0003_pages_frontpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='pages',
            name='published',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pages',
            name='content',
            field=models.TextField(default='Empty', max_length=20480),
        ),
        migrations.AlterField(
            model_name='pages',
            name='date_modified',
            field=models.DateTimeField(default=datetime.datetime.utcnow),
        ),
    ]
