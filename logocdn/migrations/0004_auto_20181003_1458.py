# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-10-03 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logocdn', '0003_auto_20181003_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logoentries',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='logocdn.LogoTags'),
        ),
    ]
