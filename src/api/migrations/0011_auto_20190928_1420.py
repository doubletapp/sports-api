# Generated by Django 2.2.5 on 2019-09-28 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20190928_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='highlightfragment',
            name='start_time',
            field=models.FloatField(),
        ),
    ]