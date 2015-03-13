# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yacms', '0003_auto_20150308_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmsentries',
            name='content',
            field=models.ManyToManyField(to='yacms.CMSContents'),
            preserve_default=True,
        ),
    ]
