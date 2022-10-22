from decimal import Decimal
import datetime
from email.policy import default
from enum import unique
from string import digits
from wsgiref.validate import validator

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import pre_save, post_save, m2m_changed

from encrypted_model_fields.fields import EncryptedCharField
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError

def only_int(value): 
    if value.isdigit()==False:
        raise ValidationError('ID contains characters')

day_list = [("{:02d}".format(each), "{:02d}".format(each)) for each in range(1, 32)]
month_list = [('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'), ('05', 'May'), ('06', 'Jun'), ('07', 'July'), ('08', 'August'), ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')]
year_list = [(str(each), str(each)) for each in range(int(datetime.date.today().strftime('%Y')), 2300 + 1)]

# Create your models here.   

class Supplier(models.Model):
    Username = models.CharField(max_length=255, null=False, unique=True)

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
    Percent =  models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=70)

    def __str__(self):
        return self.Name


class Shop_data(models.Model):
    Phone =         EncryptedCharField(blank=False, null=False, max_length=25, validators=[only_int], unique=True)
    Exp_day =       models.CharField(choices=day_list, blank=True, null=True, max_length=2, validators=[only_int])
    Exp_month =     models.CharField(choices=month_list, blank=True, null=True, max_length=2, validators=[only_int])
    Exp_year =      models.CharField(choices=year_list, blank=True, null=True, max_length=4, validators=[only_int])
    Puk_code =      models.CharField(max_length=8, blank=True, null=True, validators=[only_int])
    First_name =    models.CharField(max_length=100, blank=True, null=True)
    Last_name =     models.CharField(max_length=100, blank=True, null=True)
    Gender =        models.CharField(default='Unknown', choices=[('Male', 'Male'), ('Female', 'Female'), ('Unknown', 'Unknown')], max_length=7, blank=True, null=False)
    Address =       models.CharField(max_length=255, blank=True, null=True)
    City =          models.CharField(max_length=100, blank=True, null=False, default='')
    State =         models.CharField(max_length=100, blank=True, null=False, default='')
    Zipcode =       models.CharField(max_length=50, blank=True, null=True)
    Extra1 =        models.CharField(max_length=255, blank=True, null=True)
    Extra2 =        models.CharField(max_length=255, blank=True, null=True)
    Extra3 =        models.CharField(max_length=255, blank=True, null=True)
    Extra4 =        models.CharField(max_length=255, blank=True, null=True)
    Extra5 =        models.CharField(max_length=255, blank=True, null=True)
    Price =         models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=False, default=0)
    Batch =         models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='batch_product_list', null=False)

    Areaf1 =        models.CharField(max_length=255, blank=True, null=False, default='')
    Areaf2 =        models.CharField(max_length=255, blank=True, null=False, default='')
    Areaf3 =        models.CharField(max_length=255, blank=True, null=False, default='')
    Areaf4 =        models.CharField(max_length=255, blank=True, null=False, default='')
    Areaf5 =        models.CharField(max_length=255, blank=True, null=False, default='')
    Areaf6 =        models.CharField(max_length=255, blank=True, null=False, default='')
    Area_code =     models.CharField(max_length=6, null=False, validators=[only_int])

    Sold_unsold =   models.CharField(choices=[
        ('UNSOLD', 'UNSOLD'),
        ('SOLD', 'SOLD'),
        ('REFUND', 'REFUND'),
        ('ON_CART', 'ON_CART'),
        ('CHECKING', 'CHECKING')
        ], default='UNSOLD', max_length=8, blank=True, null=False)
    Insert_date =   models.DateTimeField(auto_now_add=True)
    Sold_date =     models.DateTimeField(blank=True, null=True)
    Supplier_payment_status = models.CharField(choices=[
                            ('PAID', 'PAID'),
                            ('UNPAID', 'UNPAID')
                            ], max_length=8, default='UNPAID')
    User =          models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.Area_code)
        

class CartManager(models.Manager):
    def new_or_get(self, request):
        qs = self.get_queryset().filter(user=request.user)
        if qs.count() == 1:
            cart_obj = qs.first()
        else:
            cart_obj = Cart.objects.create(user=request.user)
        return cart_obj


class Cart(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    products    = models.ManyToManyField(Shop_data,
                                         blank=True)
    subtotal    = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    total       = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':        
        # total = instance.products.aggregate(total_price=Sum('Shop_data__Price'))['total_price']
        products = instance.products.all()
        total = 0
        for each in products:
            total += float(each.Price)
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = Decimal(instance.subtotal) * Decimal(1.08) # 8% tax
    else:
        instance.total = 0.00

pre_save.connect(pre_save_cart_receiver, sender=Cart)


class Order_history(models.Model):
    User =          models.ForeignKey(User, on_delete=models.CASCADE)
    Product = models.OneToOneField(Shop_data, on_delete=models.CASCADE)

    Checker = models.ForeignKey(Checker, on_delete=models.CASCADE)
    Checker_status = models.CharField(choices=[
                            ('Done', 'Done'),
                            ('Fail', 'Fail')
                            ], max_length=12, default='Done')
    Checker_response_text = models.TextField()
    Checker_response_full = models.TextField()
    Checker_date = models.DateTimeField(auto_created=True, auto_now=True)


class StoreInfoManage(models.Model):
    Store_Info = RichTextField()

    def __str__(self):
        return "Store Info Manage"


class SupplierRequest(models.Model):
    Supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    Date = models.DateTimeField(auto_now_add=True, null=False)
    USDT_address = models.CharField(default='', max_length=255, blank=True, null=False)
    TXID = models.CharField(default='', max_length=255, blank=True, null=False)
    Status = models.CharField(choices=[
                            ('PAID', 'PAID'),
                            ('UNPAID', 'UNPAID')
                            ], max_length=8, default='UNPAID')

    def __str__(self):
        return self.Supplier.Username + ' ' + self.Date.strftime('%m/%d/%Y')