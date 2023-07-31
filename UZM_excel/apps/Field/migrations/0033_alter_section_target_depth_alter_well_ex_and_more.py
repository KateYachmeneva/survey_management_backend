# Generated by Django 4.0.3 on 2023-07-10 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Field', '0032_alter_well_comment_alter_well_mail_cc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='target_depth',
            field=models.FloatField(blank=True, null=True, verbose_name='Плановая глубина секции, м'),
        ),
        migrations.AlterField(
            model_name='well',
            name='EX',
            field=models.FloatField(blank=True, null=True, verbose_name='Долгота (прямоугольные координаты), м'),
        ),
        migrations.AlterField(
            model_name='well',
            name='NY',
            field=models.FloatField(blank=True, null=True, verbose_name='Широта (прямоугольные координаты), м'),
        ),
        migrations.AlterField(
            model_name='well',
            name='RKB',
            field=models.FloatField(blank=True, default=84, null=True, verbose_name='Альтитуда стола ротора, м'),
        ),
        migrations.AlterField(
            model_name='well',
            name='active_from',
            field=models.FloatField(blank=True, null=True, verbose_name='Глубина начала активной фазы, м'),
        ),
        migrations.AlterField(
            model_name='well',
            name='btotal',
            field=models.FloatField(blank=True, null=True, verbose_name='Напряженность геомагнитного поля, нТл'),
        ),
        migrations.AlterField(
            model_name='well',
            name='dec',
            field=models.FloatField(blank=True, null=True, verbose_name='Магнитное склонение, град'),
        ),
        migrations.AlterField(
            model_name='well',
            name='dip',
            field=models.FloatField(blank=True, null=True, verbose_name='Магнитное наклонение, град'),
        ),
        migrations.AlterField(
            model_name='well',
            name='grid_convergence',
            field=models.FloatField(blank=True, null=True, verbose_name='Сближение меридианов, град'),
        ),
        migrations.AlterField(
            model_name='well',
            name='gtotal',
            field=models.FloatField(blank=True, null=True, verbose_name='Напряженность гравитационного поля, G'),
        ),
        migrations.AlterField(
            model_name='well',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Широта (ось Y)'),
        ),
        migrations.AlterField(
            model_name='well',
            name='longtitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Долгота (ось X)'),
        ),
        migrations.AlterField(
            model_name='well',
            name='status_drilling',
            field=models.CharField(blank=True, choices=[('ACTV', 'Активная фаза'), ('NOACT', 'Неактивная стадия')], max_length=5, null=True, verbose_name='Статус бурения'),
        ),
        migrations.AlterField(
            model_name='well',
            name='total_correction',
            field=models.FloatField(blank=True, null=True, verbose_name='Общая поправка, град'),
        ),
        migrations.AlterField(
            model_name='wellbore',
            name='wellbore',
            field=models.CharField(choices=[('PLT0', 'ПЛ'), ('PLT1', 'ПЛ1'), ('PLT2', 'ПЛ2'), ('MAIN', 'Основной ствол'), ('BGS0', 'БГС'), ('ST01', 'СТ1'), ('ST02', 'СТ2'), ('ST03', 'СТ3'), ('ST04', 'СТ4'), ('BS01', 'БС1'), ('BS02', 'БС2'), ('BS03', 'БС3'), ('BS04', 'БС4'), ('BS05', 'БС5'), ('BS06', 'БС6'), ('BS07', 'БС7'), ('BS08', 'БС8')], max_length=4, verbose_name='Ствол'),
        ),
    ]