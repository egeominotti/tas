# Generated by Django 3.2.6 on 2021-08-09 01:40

from django.db import migrations, models
import django.db.models.deletion
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0007_delete_toimportcoins'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogicEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('flgEnable', models.BooleanField(default=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('ratio', models.FloatField(default=0)),
                ('sleep', models.IntegerField(default=0)),
                ('function', django_quill.fields.QuillField(blank=True)),
            ],
            options={
                'verbose_name': 'LogicEntry',
                'verbose_name_plural': 'LogicEntry',
            },
        ),
        migrations.CreateModel(
            name='LogicExit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('flgEnable', models.BooleanField(default=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('takeprofit', models.FloatField(default=0)),
                ('stoploss', models.FloatField(default=0)),
                ('function', django_quill.fields.QuillField(blank=True)),
            ],
            options={
                'verbose_name': 'LogicExit',
                'verbose_name_plural': 'LogicExit',
            },
        ),
        migrations.AlterField(
            model_name='strategybacktesting',
            name='logic_entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backtest.logicentry'),
        ),
        migrations.AlterField(
            model_name='strategybacktesting',
            name='logic_exit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backtest.logicexit'),
        ),
    ]