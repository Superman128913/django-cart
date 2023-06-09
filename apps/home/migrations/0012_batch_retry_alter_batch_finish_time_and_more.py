# Generated by Django 4.0.4 on 2022-07-12 14:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_remove_site_manage_uner_mantatince_messge_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='retry',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='batch',
            name='finish_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 12, 23, 4, 17, 591493)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='start_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 12, 23, 4, 17, 591493)),
        ),
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 12, 23, 4, 17, 589498)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='Deposit_Received_At',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 12, 23, 4, 17, 591493)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='User_Balance_updated_At',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 12, 23, 4, 17, 591493)),
        ),
    ]
