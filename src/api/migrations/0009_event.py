# Generated by Django 2.2.5 on 2019-09-28 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20190928_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('global_id', models.CharField(max_length=255)),
                ('time', models.DateTimeField(db_index=True)),
                ('type', models.CharField(db_index=True, max_length=255)),
                ('team', models.CharField(choices=[('HOME', 'HOME'), ('AWAY', 'AWAY')], max_length=20)),
                ('match_time', models.IntegerField(null=True)),
                ('home_score', models.IntegerField(null=True)),
                ('away_score', models.IntegerField(null=True)),
                ('player_name', models.CharField(max_length=255, null=True)),
                ('player_avatar', models.CharField(max_length=255, null=True)),
                ('method_score', models.CharField(choices=[('PENALTY', 'Penalty'), ('GOAL', 'Goal'), ('OWNGOAL', 'Own goal')], max_length=255, null=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Match')),
            ],
        ),
    ]
