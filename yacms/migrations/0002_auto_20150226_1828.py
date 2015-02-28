# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yacms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CMSTags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='NotSet', max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='CMSMarkUp',
            new_name='CMSMarkUps',
        ),
        migrations.RemoveField(
            model_name='cmsentry',
            name='meta_description',
        ),
        migrations.AddField(
            model_name='cmscontents',
            name='meta_description',
            field=models.TextField(default='', max_length=20480),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cmscontents',
            name='tags',
            field=models.ManyToManyField(to='yacms.CMSTags'),
            preserve_default=True,
        ),
    ]
