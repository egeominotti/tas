# Generated by Django 3.2.5 on 2021-08-01 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0007_trendchecker_avg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trendchecker',
            name='avg',
        ),
    ]
