# Generated by Django 4.0.3 on 2023-03-07 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0011_alter_dynamicnnbdata_options_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='dynamicnnbdata',
            table='meas_dynamic_NNB',
        ),
        migrations.AlterModelTable(
            name='igirgidynamic',
            table='meas_dynamic_igirgi',
        ),
        migrations.AlterModelTable(
            name='igirgistatic',
            table='meas_static_igirgi',
        ),
        migrations.AlterModelTable(
            name='plan',
            table='meas_plan',
        ),
        migrations.AlterModelTable(
            name='raw',
            table='meas_raw',
        ),
        migrations.AlterModelTable(
            name='staticnnbdata',
            table='meas_static_NNB',
        ),
    ]
