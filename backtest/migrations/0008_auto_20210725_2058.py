# Generated by Django 3.2.5 on 2021-07-25 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0007_auto_20210724_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='backtest',
            name='candle_stop_loss_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='backtest',
            name='candle_take_profit_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
