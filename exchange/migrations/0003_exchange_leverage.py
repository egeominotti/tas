# Generated by Django 3.2.6 on 2021-08-03 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0002_user_bot'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchange',
            name='leverage',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]