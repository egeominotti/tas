# Generated by Django 3.2.6 on 2021-09-02 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0020_alter_bot_coins'),
        ('strategy', '0005_auto_20210902_2208'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Coins',
        ),
    ]
