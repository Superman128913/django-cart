# Generated by Django 3.2.4 on 2022-10-18 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0021_auto_20221018_0505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop_data',
            name='Gender',
            field=models.CharField(blank=True, choices=[('Man', 'Man'), ('Female', 'Female'), ('Unknown', 'Unknown')], default='Unknown', max_length=7),
        ),
    ]
