# Generated by Django 3.2.6 on 2021-08-07 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0024_botlogger_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botlogger',
            name='bot',
        ),
    ]
