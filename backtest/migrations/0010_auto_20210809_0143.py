# Generated by Django 3.2.6 on 2021-08-09 01:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0009_auto_20210809_0142'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logicentry',
            options={'verbose_name': 'LogicEntryBacktesting', 'verbose_name_plural': 'LogicEntryBacktesting'},
        ),
        migrations.AlterModelOptions(
            name='logicexit',
            options={'verbose_name': 'LogicExitBacktesting', 'verbose_name_plural': 'LogicExitBacktesting'},
        ),
    ]