# Generated by Django 3.2.5 on 2021-08-01 03:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0012_rename_net_profit_statisticsportfolio_current_wallet'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='backtestlog',
            options={'verbose_name': 'BacktestLog', 'verbose_name_plural': 'BacktestLog'},
        ),
        migrations.AlterModelOptions(
            name='statisticsportfolio',
            options={'verbose_name': 'StatisticsPortfolio', 'verbose_name_plural': 'StatisticsPortfolio'},
        ),
    ]