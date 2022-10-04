from django.contrib import admin
from .models import *

# Register your models here.
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['Username']


class CheckerAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Cost']


class BatchAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Publish_date', 'Supplier', 'Supplier_payment_status', 'Percent']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['Phone', 'Exp_day', 'Exp_month', 'Exp_year', 'Puk_code', 'First_name', 'Last_name', 'Gender', 'Address', 'City', 'State', 'Zipcode', 'Extra1', 'Extra2', 'Extra3', 'Extra4', 'Extra5', 'Price', 'Areaf1', 'Areaf2', 'Areaf3', 'Areaf4', 'Areaf5', 'Areaf6', 'Area_code', 'Sold_unsold', 'Insert_date', 'Sold_date']
    

class HistoryAdmin(admin.ModelAdmin):
    list_display = ['User', 'Product', 'Checker', 'Checker_status', 'Checker_response_text', 'Checker_response_full', 'Checker_date']
    

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Checker, CheckerAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Shop_data, ProductAdmin)
admin.site.register(Order_history, HistoryAdmin)