# Generated by Django 3.2.6 on 2021-08-03 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0003_auto_20210803_1845'),
        ('bot', '0003_auto_20210803_1845'),
        ('strategy', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Strategy',
        ),
    ]
