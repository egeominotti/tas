# Generated by Django 3.2.6 on 2021-08-03 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_remove_bot_user'),
        ('exchange', '0003_exchange_leverage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bot',
            field=models.ManyToManyField(blank=True, null=True, to='bot.Bot'),
        ),
    ]