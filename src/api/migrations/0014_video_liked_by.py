# Generated by Django 2.2.5 on 2019-09-28 18:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20190928_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='liked_by',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), default=[], size=None),
            preserve_default=False,
        ),
    ]