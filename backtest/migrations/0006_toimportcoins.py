# Generated by Django 3.2.6 on 2021-08-07 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('strategy', '0008_auto_20210807_2130'),
        ('backtest', '0005_alter_strategybacktesting_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToImportCoins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('flgEnable', models.BooleanField(default=True)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.symbolexchange')),
                ('time_frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategy.timeframe')),
            ],
            options={
                'verbose_name': 'ToImportCoins',
                'verbose_name_plural': 'ToImportCoins',
            },
        ),
    ]