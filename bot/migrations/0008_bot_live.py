# Generated by Django 3.2.5 on 2021-07-28 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0007_bot_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='live',
            field=models.BooleanField(default=False),
        ),
    ]
