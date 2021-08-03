# Generated by Django 3.2.6 on 2021-08-03 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('strategy', '0001_initial'),
        ('backtest', '0002_backtest_strategy'),
    ]

    operations = [
        migrations.CreateModel(
            name='StrategyBacktesting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('flgEnable', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('logic_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.logicentry')),
                ('logic_exit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.logicexit')),
                ('symbol_exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.symbolexchange')),
                ('time_frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.timeframe')),
            ],
            options={
                'verbose_name': 'Strategy',
                'verbose_name_plural': 'Strategy',
            },
        ),
        migrations.AlterField(
            model_name='backtest',
            name='strategy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backtest.strategybacktesting'),
        ),
    ]
