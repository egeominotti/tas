# Generated by Django 3.2.6 on 2021-08-08 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('strategy', '0008_auto_20210807_2130'),
        ('bot', '0036_alter_userexchange_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='BufferRecordData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('flgEnable', models.BooleanField(default=True)),
                ('time_frame', models.CharField(max_length=4)),
                ('open_candle', models.FloatField(blank=True, default=0)),
                ('close_candle', models.FloatField(blank=True, default=0)),
                ('high_candle', models.FloatField(blank=True, default=0)),
                ('low_candle', models.FloatField(blank=True, default=0)),
                ('is_closed', models.BooleanField(default=False)),
                ('symbol', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='strategy.symbolexchange')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
