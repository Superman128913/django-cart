# Generated by Django 3.2.4 on 2022-10-15 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0017_supplierrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplierrequest',
            name='Status',
            field=models.CharField(choices=[('PAID', 'PAID'), ('UNPAID', 'UNPAID')], default='UNPAID', max_length=8),
        ),
    ]