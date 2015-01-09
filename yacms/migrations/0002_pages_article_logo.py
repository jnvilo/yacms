# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yacms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pages',
            name='article_logo',
            field=models.TextField(max_length=1023, null=True, blank=True),
            preserve_default=True,
        ),
    ]
