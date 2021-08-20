# Generated by Django 3.2.6 on 2021-08-20 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0012_remove_bufferrecorddata_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='bufferrecorddata',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='bufferrecorddata',
            name='flgEnable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='bufferrecorddata',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
