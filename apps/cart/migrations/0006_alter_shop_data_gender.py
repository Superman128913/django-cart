# Generated by Django 3.2.4 on 2022-09-19 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_rename_areaf6_code_shop_data_area_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop_data',
            name='Gender',
            field=models.CharField(choices=[('M', 'Man'), ('F', 'Female')], default='M', max_length=2),
        ),
    ]
