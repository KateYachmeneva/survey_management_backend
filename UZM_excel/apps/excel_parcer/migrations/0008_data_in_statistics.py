# Generated by Django 4.0.3 on 2022-08-18 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel_parcer', '0007_alter_run_wellbore'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='in_statistics',
            field=models.BooleanField(default=1, verbose_name='Учитывать в статистике'),
            preserve_default=False,
        ),
    ]
