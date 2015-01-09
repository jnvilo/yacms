# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yacms', '0002_pages_article_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='pages',
            name='page_number',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
