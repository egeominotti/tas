# Generated by Django 3.2.6 on 2021-08-10 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_auto_20210810_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='bufferrecorddata',
            name='unix',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]