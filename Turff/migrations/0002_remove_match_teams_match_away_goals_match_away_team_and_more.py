# Generated by Django 4.1.3 on 2022-12-20 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Turff', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='teams',
        ),
        migrations.AddField(
            model_name='match',
            name='away_goals',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='away_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='away_matches', to='Turff.teams'),
        ),
        migrations.AddField(
            model_name='match',
            name='home_goals',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='home_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='home_matches', to='Turff.teams'),
        ),
    ]
