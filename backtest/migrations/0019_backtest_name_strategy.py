# Generated by Django 3.2.6 on 2021-08-09 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0018_auto_20210809_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='backtest',
            name='name_strategy',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]