import datetime
from itertools import product
from operator import mod
from tkinter import CASCADE

from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedIntegerField
from django.core.validators import MaxValueValidator, MinValueValidator
# from apps.home import models

day_list = [(each, each) for each in range(1, 32)]
month_list = [(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'Jun'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'Novemver'), (12, 'December')]
year_list = [(each, each) for each in range(int(datetime.date.today().strftime('%Y')), 2300 + 1)]

# Create your models here.   

class Supplier(models.Model):
    Username = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.Username


class Checker(models.Model):
    Name = models.CharField(max_length=255, null=False)
    Cost = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.Name


class Batch(models.Model):
    Name =    models.CharField(max_length=255, null=False)
    Publish_date =  models.DateTimeField(auto_now_add=True, null=False)
    
    Supplier =      models.ForeignKey(Supplier, on_delete=models.CASCADE)
    Supplier_payment_status = models.CharField(choices=[
                            ('Queue', 'Queue'),
                            ('Processing', 'Processing'),
                            ('Error', 'Error'),
                            ('Done', 'Done'),
                            ('Fail', 'Fail')
                            ], max_length=12, default='Queue')
    Percent =  models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=70)

    def __str__(self):
        return self.Name


class Shop_data(models.Model):
    Phone =         EncryptedIntegerField(null=False)
    Exp_day =       models.IntegerField(choices=day_list)
    Exp_month =     models.IntegerField(choices=month_list)
    Exp_year =      models.IntegerField(choices=year_list)
    Puk_code =      models.DecimalField(decimal_places=0, max_digits=8)
    First_name =    models.CharField(max_length=100)
    Last_name =     models.CharField(max_length=100)
    Gender =        models.CharField(default='M', choices=[('M', 'Man'), ('F', 'Female')], max_length=2)
    Address =       models.CharField(max_length=255)
    City =          models.CharField(max_length=100)
    State =         models.CharField(max_length=100)
    Zipcode =       models.CharField(max_length=10, null=False)
    Extra1 =        models.CharField(max_length=255)
    Extra2 =        models.CharField(max_length=255)
    Extra3 =        models.CharField(max_length=255)
    Extra4 =        models.CharField(max_length=255)
    Extra5 =        models.CharField(max_length=255)
    Price =         models.DecimalField(decimal_places=2, max_digits=10)
    Batch =         models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='batch_product_list', null=False)

    Areaf1 =        models.CharField(max_length=255, null=False)
    Areaf2 =        models.CharField(max_length=255, null=False)
    Areaf3 =        models.CharField(max_length=255, null=False)
    Areaf4 =        models.CharField(max_length=255, null=True)
    Areaf5 =        models.CharField(max_length=255, null=True)
    Areaf6 =        models.CharField(max_length=255, null=True)
    Area_code =     models.DecimalField(decimal_places=0, max_digits=6, null=False)

    Sold_unsold =   models.CharField(choices=[('UNSOLD', 'UNSOLD'), ('SOLD', 'SOLD'), ('REFUND', 'REFUND')], default='UNSOLD', max_length=7)
    Insert_date =   models.DateTimeField(auto_now_add=True, null=False)
    Sold_date =     models.DateTimeField(null=True)
    User =          models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.Area_code)


# class Cart(models.Model):
#     User =          models.ForeignKey(User, on_delete=models.CASCADE)
#     Product = models.ForeignKey(Shop_data, on_delete=models.CASCADE)

#     Checker = models.ForeignKey(Checker, on_delete=models.CASCADE)
#     Checker_status = models.CharField(choices=[
#                             ('Queue', 'Queue'),
#                             ('Processing', 'Processing'),
#                             ('Error', 'Error'),
#                             ('Done', 'Done'),
#                             ('Fail', 'Fail')
#                             ], max_length=12, default='Queue')
#     Checker_response_text = models.TextField()
#     Checker_response_full = models.TextField()
#     Checker_date = models.DateTimeField(auto_created=True, auto_now=True)