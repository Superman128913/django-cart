# Generated by Django 3.2.4 on 2022-10-18 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0024_alter_shop_data_zipcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop_data',
            name='Areaf1',
            field=models.CharField(blank=True, default='Other', max_length=255),
        ),
        migrations.AlterField(
            model_name='shop_data',
            name='Areaf2',
            field=models.CharField(blank=True, default='Other', max_length=255),
        ),
        migrations.AlterField(
            model_name='shop_data',
            name='Areaf3',
            field=models.CharField(blank=True, default='Other', max_length=255),
        ),
        migrations.AlterField(
            model_name='shop_data',
            name='Areaf4',
            field=models.CharField(blank=True, default='Other', max_length=255),
        ),
        migrations.AlterField(
            model_name='shop_data',
            name='Areaf5',
            field=models.CharField(blank=True, default='Other', max_length=255),
        ),
        migrations.AlterField(
            model_name='shop_data',
            name='Areaf6',
            field=models.CharField(blank=True, default='Other', max_length=255),
        ),
    ]
