# Generated by Django 4.0.3 on 2023-07-12 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Field', '0034_alter_client_client_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='client_name',
            field=models.CharField(choices=[('SMTL', 'Самотлорнефтегаз'), ('SKNG', 'Севкомнефтегаз'), ('UVAT', 'Уватнефтегаз'), ('SBNG', 'Сибнефтегаз'), ('UDMR', 'Удмуртнефть'), ('TUNG', 'ТЮНГ'), ('UGNG', 'Юганскнефтегаз'), ('SLN', 'Славнефть'), ('CHNG', 'Харампурнефтегаз'), ('RNHA', 'РНША'), ('VOIL', 'Восток Ойл'), ('PRNG', 'Пурнефтегаз'), ('VCNG', 'ВЧНГ')], max_length=4, unique=True, verbose_name='Заказчик'),
        ),
    ]