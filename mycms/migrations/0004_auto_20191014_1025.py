# Generated by Django 2.2.6.dev20190909114231 on 2019-10-14 10:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mycms', '0003_auto_20191014_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]