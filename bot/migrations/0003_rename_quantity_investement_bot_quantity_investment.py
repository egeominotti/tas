# Generated by Django 3.2.5 on 2021-07-29 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_remove_bot_indicators'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bot',
            old_name='quantity_investement',
            new_name='quantity_investment',
        ),
    ]