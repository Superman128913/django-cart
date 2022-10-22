# Generated by Django 3.2.4 on 2022-10-20 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0028_alter_order_history_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop_data',
            name='Sold_unsold',
            field=models.CharField(blank=True, choices=[('UNSOLD', 'UNSOLD'), ('SOLD', 'SOLD'), ('REFUND', 'REFUND'), ('ON_CART', 'ON_CART'), ('CHECKING', 'CHECKING')], default='UNSOLD', max_length=8),
        ),
    ]
