# Generated by Django 4.0.3 on 2022-09-05 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel_parcer', '0009_remove_run_device'),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depth', models.TextField(max_length=200, verbose_name='Глубина')),
                ('CX', models.TextField(max_length=200, verbose_name='GX')),
                ('CY', models.TextField(max_length=200, verbose_name='GY')),
                ('CZ', models.TextField(max_length=200, verbose_name='GZ')),
                ('BX', models.TextField(max_length=200, verbose_name='BX')),
                ('BY', models.TextField(max_length=200, verbose_name='BY')),
                ('BZ', models.TextField(max_length=200, verbose_name='BZ')),
            ],
            options={
                'verbose_name': 'Лист заголовков',
                'verbose_name_plural': 'Листы заголовков',
            },
        ),
    ]
