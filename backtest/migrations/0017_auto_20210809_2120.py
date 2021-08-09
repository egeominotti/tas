# Generated by Django 3.2.6 on 2021-08-09 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('strategy', '0009_auto_20210809_0149'),
        ('backtest', '0016_backtest_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='backtest',
            name='strategy',
        ),
        migrations.AddField(
            model_name='backtest',
            name='logic_entry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backtest.logicentry'),
        ),
        migrations.AddField(
            model_name='backtest',
            name='logic_exit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backtest.logicexit'),
        ),
        migrations.AddField(
            model_name='backtest',
            name='symbol',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='strategy.symbolexchange'),
        ),
        migrations.AddField(
            model_name='backtest',
            name='time_frame',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='strategy.timeframe'),
        ),
        migrations.DeleteModel(
            name='StrategyBacktesting',
        ),
    ]