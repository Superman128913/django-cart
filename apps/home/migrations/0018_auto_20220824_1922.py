# Generated by Django 3.2.4 on 2022-08-24 19:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_auto_20220720_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesslog',
            name='last_ticket_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 24, 19, 22, 47, 222909)),
        ),
        migrations.AlterField(
            model_name='accesslog',
            name='last_view_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 24, 19, 22, 47, 222894)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='finish_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 8, 24, 19, 22, 47, 220955)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='start_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 8, 24, 19, 22, 47, 220943)),
        ),
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 8, 24, 19, 22, 47, 219262)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='Deposit_Received_At',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 8, 24, 19, 22, 47, 220511)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='User_Balance_updated_At',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 8, 24, 19, 22, 47, 220533)),
        ),
    ]
