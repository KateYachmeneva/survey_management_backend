# Generated by Django 4.0.3 on 2023-02-15 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Field', '0002_alter_client_options_alter_contractor_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Дочернее общество', 'verbose_name_plural': 'Дочерние общества'},
        ),
        migrations.AlterModelOptions(
            name='contractor',
            options={'verbose_name': 'Подрядчик', 'verbose_name_plural': 'Подрядчики'},
        ),
        migrations.AlterModelOptions(
            name='field',
            options={'verbose_name': 'Месторождение', 'verbose_name_plural': 'Месторождения'},
        ),
        migrations.AlterModelOptions(
            name='pad',
            options={'verbose_name': 'Куст', 'verbose_name_plural': 'Кусты'},
        ),
        migrations.AlterModelOptions(
            name='run',
            options={'verbose_name': 'Рейс', 'verbose_name_plural': 'Рейсы'},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'verbose_name': 'Секция', 'verbose_name_plural': 'Секции'},
        ),
        migrations.AlterModelOptions(
            name='well',
            options={'verbose_name': 'Скважина', 'verbose_name_plural': 'Скважины'},
        ),
        migrations.AlterModelOptions(
            name='wellbore',
            options={'verbose_name': 'Ствол', 'verbose_name_plural': 'Стволы'},
        ),
        migrations.AlterModelTable(
            name='client',
            table=None,
        ),
        migrations.AlterModelTable(
            name='contractor',
            table=None,
        ),
    ]
