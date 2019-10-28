# Generated by Django 2.2.6.dev20190909114231 on 2019-10-18 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("mycms", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="CMSModelField",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=92)),
                (
                    "node",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="mycms.Node"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CMSContentModelField",
            fields=[
                (
                    "cmsmodelfield_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="mycms.CMSModelField",
                    ),
                ),
                (
                    "content",
                    models.TextField(default="No Content", max_length=4096, null=True),
                ),
            ],
            bases=("mycms.cmsmodelfield",),
        ),
    ]