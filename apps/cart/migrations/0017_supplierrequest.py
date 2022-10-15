# Generated by Django 3.2.4 on 2022-10-15 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0016_auto_20221014_0327'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateTimeField(auto_now_add=True)),
                ('USDT_address', models.CharField(blank=True, default='', max_length=255)),
                ('TXID', models.CharField(blank=True, default='', max_length=255)),
                ('Supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.supplier')),
            ],
        ),
    ]