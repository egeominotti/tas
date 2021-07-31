# Generated by Django 3.2.5 on 2021-07-30 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0010_statisticsportfolio_initial_investment'),
    ]

    operations = [
        migrations.AddField(
            model_name='backtestlog',
            name='loss_percentage',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='backtestlog',
            name='profit_percentage',
            field=models.FloatField(blank=True, default=0),
        ),
    ]