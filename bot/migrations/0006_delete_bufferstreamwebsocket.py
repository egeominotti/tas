# Generated by Django 3.2.6 on 2021-08-12 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_alter_bufferrecorddata_unix'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BufferStreamWebSocket',
        ),
    ]
