from decimal import Decimal
import datetime

from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedBigIntegerField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.db.models import Sum
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
    Phone =         EncryptedBigIntegerField(blank=False)
    Exp_day =       models.IntegerField(choices=day_list)
    Exp_month =     models.IntegerField(choices=month_list)
    Exp_year =      models.IntegerField(choices=year_list)
    Puk_code =      models.DecimalField(decimal_places=0, max_digits=8)
    First_name =    models.CharField(max_length=100)
    Last_name =     models.CharField(max_length=100)
    Gender =        models.CharField(default='U', choices=[('M', 'Man'), ('F', 'Female'), ('U', 'Unknown')], max_length=2, blank=True, null=False)
    Address =       models.CharField(max_length=255)
    City =          models.CharField(max_length=100)
    State =         models.CharField(max_length=100)
    Zipcode =       models.CharField(max_length=10, blank=False)
    Extra1 =        models.CharField(max_length=255, blank=True, null=False, default='')
    Extra2 =        models.CharField(max_length=255, blank=True, null=False, default='')
    Extra3 =        models.CharField(max_length=255, blank=True, null=False, default='')
    Extra4 =        models.CharField(max_length=255, blank=True, null=False, default='')
    Extra5 =        models.CharField(max_length=255, blank=True, null=False, default='')
    Price =         models.DecimalField(decimal_places=2, max_digits=10)
    Batch =         models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='batch_product_list', null=False)

    Areaf1 =        models.CharField(max_length=255, null=False)
    Areaf2 =        models.CharField(max_length=255, null=False)
    Areaf3 =        models.CharField(max_length=255, null=False)
    Areaf4 =        models.CharField(max_length=255, blank=True)
    Areaf5 =        models.CharField(max_length=255, blank=True)
    Areaf6 =        models.CharField(max_length=255, blank=True)
    Area_code =     models.DecimalField(decimal_places=0, max_digits=6, null=False)

    Sold_unsold =   models.CharField(choices=[
        ('UNSOLD', 'UNSOLD'),
        ('SOLD', 'SOLD'),
        ('REFUND', 'REFUND'),
        ('ON_CART', 'ON_CART')
        ], default='UNSOLD', max_length=7)
    Insert_date =   models.DateTimeField(auto_now_add=True)
    Sold_date =     models.DateTimeField(blank=True, null=True)
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
    Product = models.ForeignKey(Shop_data, on_delete=models.CASCADE)

    Checker = models.ForeignKey(Checker, on_delete=models.CASCADE)
    Checker_status = models.CharField(choices=[
                            ('Done', 'Done'),
                            ('Fail', 'Fail')
                            ], max_length=12, default='Done')
    Checker_response_text = models.TextField()
    Checker_response_full = models.TextField()
    Checker_date = models.DateTimeField(auto_created=True, auto_now=True)