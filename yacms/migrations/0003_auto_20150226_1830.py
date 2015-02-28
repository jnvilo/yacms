# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yacms', '0002_auto_20150226_1828'),
    ]

    operations = [
        migrations.CreateModel(
            name='CMSEntries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=None, max_length=1024)),
                ('path', models.CharField(default='/', max_length=2000)),
                ('slug', models.SlugField(max_length=1024)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('frontpage', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=False)),
                ('page_number', models.IntegerField(default=1)),
                ('content', models.ManyToManyField(to='yacms.CMSContents', null=True)),
                ('page_type', models.ForeignKey(to='yacms.CMSPageTypes', null=True)),
                ('template', models.ForeignKey(to='yacms.CMSTemplates', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='cmsentry',
            name='content',
        ),
        migrations.RemoveField(
            model_name='cmsentry',
            name='page_type',
        ),
        migrations.RemoveField(
            model_name='cmsentry',
            name='template',
        ),
        migrations.DeleteModel(
            name='CMSEntry',
        ),
    ]
