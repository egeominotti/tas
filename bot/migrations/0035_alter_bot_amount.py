# Generated by Django 3.2.6 on 2021-08-08 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0034_alter_bot_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='amount',
            field=models.FloatField(default=11),
        ),
    ]