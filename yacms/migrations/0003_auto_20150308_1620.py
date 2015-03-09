# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yacms', '0002_auto_20150304_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmsentries',
            name='slug',
            field=models.SlugField(max_length=1024, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cmsentries',
            name='template',
            field=models.ForeignKey(blank=True, to='yacms.CMSTemplates', null=True),
            preserve_default=True,
        ),
    ]
