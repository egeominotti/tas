# Generated by Django 3.2.5 on 2021-07-30 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0004_auto_20210730_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='backtest',
            name='scheduled',
            field=models.BooleanField(default=False),
        ),
    ]