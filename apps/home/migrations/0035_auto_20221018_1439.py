# Generated by Django 3.2.4 on 2022-10-18 18:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0034_auto_20221018_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesslog',
            name='last_ticket_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 18, 14, 39, 40, 845765)),
        ),
        migrations.AlterField(
            model_name='accesslog',
            name='last_view_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 18, 14, 39, 40, 845765)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='finish_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 18, 14, 39, 40, 824759)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='start_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 18, 14, 39, 40, 824759)),
        ),
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 18, 14, 39, 40, 792763)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='Deposit_Received_At',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 18, 14, 39, 40, 820761)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='User_Balance_updated_At',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 18, 14, 39, 40, 820761)),
        ),
    ]