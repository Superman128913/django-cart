# Generated by Django 3.2.4 on 2022-09-16 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Exp_day',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='Exp_month',
            field=models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'Jun'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'Novemver'), (12, 'December')]),
        ),
        migrations.AlterField(
            model_name='product',
            name='Exp_year',
            field=models.IntegerField(choices=[(2021, 2021)]),
        ),
    ]
