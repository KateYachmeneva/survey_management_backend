# Generated by Django 4.0.3 on 2023-08-28 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Field', '0041_wellbore_igirgi_drilling'),
    ]

    operations = [
        migrations.AddField(
            model_name='wellbore',
            name='current_depth',
            field=models.FloatField(blank=True, null=True, verbose_name='Текущая глубина, м'),
        ),
    ]
