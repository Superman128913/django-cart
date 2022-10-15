# Generated by Django 3.2.4 on 2022-10-15 18:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_auto_20221014_0327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesslog',
            name='last_ticket_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 15, 14, 7, 55, 820574)),
        ),
        migrations.AlterField(
            model_name='accesslog',
            name='last_view_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 15, 14, 7, 55, 820574)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='finish_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 15, 14, 7, 55, 815571)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='start_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 15, 14, 7, 55, 815571)),
        ),
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 15, 14, 7, 55, 808565)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='Deposit_Received_At',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 15, 14, 7, 55, 814573)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='User_Balance_updated_At',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 15, 14, 7, 55, 814573)),
        ),
    ]
