# Generated by Django 3.2.5 on 2021-07-28 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0013_auto_20210728_0348'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='leverage',
            field=models.IntegerField(default=0),
        ),
    ]
