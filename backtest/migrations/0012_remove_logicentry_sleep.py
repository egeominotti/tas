# Generated by Django 3.2.6 on 2021-08-09 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0011_auto_20210809_0143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logicentry',
            name='sleep',
        ),
    ]
