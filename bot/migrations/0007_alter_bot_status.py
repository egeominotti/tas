# Generated by Django 3.2.5 on 2021-08-02 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_auto_20210802_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='status',
            field=models.CharField(choices=[('STOPPED', 'STOPPED'), ('RUNNING', 'RUNNING')], default='STOPPED', max_length=50),
        ),
    ]