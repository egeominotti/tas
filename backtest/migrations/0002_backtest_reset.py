# Generated by Django 3.2.6 on 2021-08-09 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='backtest',
            name='reset',
            field=models.BooleanField(default=False),
        ),
    ]
