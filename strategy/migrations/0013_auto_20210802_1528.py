# Generated by Django 3.2.5 on 2021-08-02 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('strategy', '0012_auto_20210802_1522'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='symbolexchange',
            options={'verbose_name': 'SymbolExchange', 'verbose_name_plural': 'SymbolExchange'},
        ),
        migrations.AlterModelOptions(
            name='symboltaapiapi',
            options={'verbose_name': 'SymbolTaapiApi', 'verbose_name_plural': 'SymbolTaapiApi'},
        ),
    ]
