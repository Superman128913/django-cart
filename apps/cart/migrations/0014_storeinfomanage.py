# Generated by Django 3.2.4 on 2022-10-08 19:56

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0013_auto_20221005_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreInfoManage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Store_Info', ckeditor.fields.RichTextField()),
            ],
        ),
    ]
