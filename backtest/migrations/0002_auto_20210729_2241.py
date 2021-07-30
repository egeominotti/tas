# Generated by Django 3.2.5 on 2021-07-29 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogicEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('flgEnable', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LogicStopLoss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('flgEnable', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LogicTakepProfit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('flgEnable', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='strategy',
            name='logic_entry_function',
        ),
        migrations.RemoveField(
            model_name='strategy',
            name='logic_stoploss_function',
        ),
        migrations.RemoveField(
            model_name='strategy',
            name='logic_takeprofit_function',
        ),
        migrations.AddField(
            model_name='strategy',
            name='logic_entry',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='backtest.logicentry'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='strategy',
            name='logic_stoploss',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='backtest.logicstoploss'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='strategy',
            name='logic_takeprofit',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='backtest.logictakepprofit'),
            preserve_default=False,
        ),
    ]