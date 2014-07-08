# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yacms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paths',
            name='parent',
            field=models.ForeignKey(to='yacms.Paths', null=True),
            preserve_default=True,
        ),
    ]
