# Generated by Django 4.0.3 on 2023-08-08 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Field', '0038_wellsummary'),
    ]

    operations = [
        migrations.AddField(
            model_name='well',
            name='igirgi_drilling',
            field=models.BooleanField(blank=True, default=False, verbose_name='Бурение по таектории ИГиРГИ'),
        ),
    ]