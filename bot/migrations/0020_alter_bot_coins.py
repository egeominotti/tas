# Generated by Django 3.2.6 on 2021-09-02 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('strategy', '0005_auto_20210902_2208'),
        ('bot', '0019_clusterbot_profit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='coins',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.symbolexchange'),
        ),
    ]
