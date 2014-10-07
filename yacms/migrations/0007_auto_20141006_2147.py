# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yacms', '0006_pages_article_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paths',
            name='path',
            field=models.CharField(default='/', unique=True, max_length=1024),
        ),
    ]
