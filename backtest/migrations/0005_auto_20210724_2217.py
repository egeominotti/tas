# Generated by Django 3.2.5 on 2021-07-24 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0004_backtest'),
    ]

    operations = [
        migrations.AddField(
            model_name='backtest',
            name='candle_stop_loss',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='backtest',
            name='candle_take_profit',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
