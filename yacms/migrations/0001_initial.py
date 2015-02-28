# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CMSContents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(default='Empty', max_length=20480)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CMSEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=None, max_length=1024)),
                ('path', models.CharField(default='/', max_length=2000)),
                ('slug', models.SlugField(max_length=1024)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('frontpage', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=False)),
                ('meta_description', models.TextField(default='', max_length=20480)),
                ('page_number', models.IntegerField(default=1)),
                ('content', models.ManyToManyField(to='yacms.CMSContents', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CMSMarkUp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('markup', models.CharField(default='Creole', max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CMSPageTypes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_type', models.CharField(default='DefaultType', max_length=64)),
                ('text', models.CharField(default='default class', max_length=128)),
                ('view_class', models.CharField(default='DefaultView', max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CMSTemplates',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='page.html', max_length=1024)),
                ('template', models.TextField(default='empty template', max_length=10240)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='cmsentry',
            name='page_type',
            field=models.ForeignKey(to='yacms.CMSPageTypes', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cmsentry',
            name='template',
            field=models.ForeignKey(to='yacms.CMSTemplates', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cmscontents',
            name='markup',
            field=models.ForeignKey(to='yacms.CMSMarkUp', null=True),
            preserve_default=True,
        ),
    ]
