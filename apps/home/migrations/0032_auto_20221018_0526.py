# Generated by Django 3.2.4 on 2022-10-18 09:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0031_auto_20221018_0522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesslog',
            name='last_ticket_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 18, 5, 26, 42, 286320)),
        ),
        migrations.AlterField(
            model_name='accesslog',
            name='last_view_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 18, 5, 26, 42, 286320)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='finish_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 18, 5, 26, 42, 280316)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='start_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 18, 5, 26, 42, 280316)),
        ),
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 18, 5, 26, 42, 276314)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='Deposit_Received_At',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 18, 5, 26, 42, 279316)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='User_Balance_updated_At',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 18, 5, 26, 42, 279316)),
        ),
    ]
