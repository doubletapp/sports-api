# Generated by Django 2.2.5 on 2019-09-28 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_highlight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='highlight',
            name='fragments',
        ),
        migrations.CreateModel(
            name='HighlightFragment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('second', models.IntegerField()),
                ('highlight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Highlight')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Video')),
            ],
        ),
    ]
