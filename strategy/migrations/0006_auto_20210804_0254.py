# Generated by Django 3.2.6 on 2021-08-04 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('strategy', '0005_auto_20210804_0243'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logicexit',
            old_name='stop_loss_long',
            new_name='stoploss_long',
        ),
        migrations.RenameField(
            model_name='logicexit',
            old_name='stop_loss_short',
            new_name='stoploss_short',
        ),
        migrations.RenameField(
            model_name='logicexit',
            old_name='take_profit_long',
            new_name='takeprofit_long',
        ),
        migrations.RenameField(
            model_name='logicexit',
            old_name='take_profit_short',
            new_name='takeprofit_short',
        ),
    ]