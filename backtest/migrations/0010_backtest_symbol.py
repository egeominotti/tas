# Generated by Django 3.2.5 on 2021-07-27 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0009_backtest_profit_loss'),
    ]

    operations = [
        migrations.AddField(
            model_name='backtest',
            name='symbol',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]