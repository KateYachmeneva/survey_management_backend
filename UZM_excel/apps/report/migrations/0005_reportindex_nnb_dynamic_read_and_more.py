# Generated by Django 4.0.3 on 2023-01-27 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0004_reportindex_run'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportindex',
            name='nnb_dynamic_read',
            field=models.CharField(max_length=10, null=True, verbose_name='Динамические от ННБ метры с которых счтываем'),
        ),
        migrations.AddField(
            model_name='reportindex',
            name='nnb_static_read',
            field=models.CharField(max_length=10, null=True, verbose_name='Статические от ННБ метры с которых счтываем'),
        ),
    ]
