# Generated by Django 3.2.6 on 2021-08-19 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0011_alter_bufferrecorddata_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bufferrecorddata',
            name='timestamp',
        ),
    ]