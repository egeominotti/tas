# Generated by Django 3.2.5 on 2021-08-01 03:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_alter_bot_binance_account'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bot',
            old_name='binance_account',
            new_name='exchange',
        ),
    ]
