# Generated by Django 4.0.4 on 2022-07-11 05:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_balance_balance_alter_batch_finish_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='finish_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 11, 14, 11, 55, 770646)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='start_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 11, 14, 11, 55, 770646)),
        ),
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 11, 14, 11, 55, 768646)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='Deposit_Received_At',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 11, 14, 11, 55, 769644)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='User_Balance_updated_At',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 11, 14, 11, 55, 769644)),
        ),
    ]
