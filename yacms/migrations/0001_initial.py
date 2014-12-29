# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1024)),
                ('slug', models.SlugField(max_length=1024)),
                ('content', models.TextField(default='Empty', max_length=20480)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('page_type', models.CharField(default='HTML', max_length=255)),
                ('template', models.CharField(default=None, max_length=244)),
                ('frontpage', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=False)),
                ('meta_description', models.TextField(default='', max_length=20480)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Paths',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(default='/', unique=True, max_length=1024)),
                ('parent', models.ForeignKey(to='yacms.Paths', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pages',
            name='path',
            field=models.ForeignKey(to='yacms.Paths', null=True),
            preserve_default=True,
        ),
    ]
