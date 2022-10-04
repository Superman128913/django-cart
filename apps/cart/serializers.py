from email.policy import default
from rest_framework import serializers
from .models import Order_history, Shop_data
from encrypted_model_fields.fields import EncryptedIntegerField


class ProductSerializer(serializers.ModelSerializer):
    Gender = serializers.SerializerMethodField()
    Batch_id = serializers.IntegerField(source='Batch.id')
    Batch_Name = serializers.CharField(source='Batch.Name')
    Batch_Publish_date = serializers.DateTimeField(source='Batch.Publish_date')

    class Meta:
        model = Shop_data
        fields = ['id', 'Area_code', 'Exp_day', 'Exp_month', 'Exp_year', 'Areaf1', 'Areaf2', 'Areaf3', 'Areaf4', 'Areaf5', 'Areaf6', 'City', 'State', 'Zipcode', 'First_name', 'Gender', 'Extra1', 'Extra2', 'Extra3', 'Extra4', 'Extra5', 'Batch_id', 'Batch_Name', 'Batch_Publish_date', 'Price']

    def get_Gender(self,obj):
        if obj.Gender == 'M':
            return 'Male'
        elif obj.Gender == 'F':
            return 'Female'
        elif obj.Gender == 'M':
            return 'Unknown'


class Areaf1Serializer(serializers.ModelSerializer):
    product_num = serializers.IntegerField(default=0)
    class Meta:
        model = Shop_data
        fields = ['Areaf1', 'product_num']


class Areaf2Serializer(serializers.ModelSerializer):
    product_num = serializers.IntegerField(default=0)
    class Meta:
        model = Shop_data
        fields = ['Areaf2', 'product_num']


class Areaf3Serializer(serializers.ModelSerializer):
    product_num = serializers.IntegerField(default=0)
    class Meta:
        model = Shop_data
        fields = ['Areaf3', 'product_num']


class Areaf4Serializer(serializers.ModelSerializer):
    product_num = serializers.IntegerField(default=0)
    class Meta:
        model = Shop_data
        fields = ['Areaf4', 'product_num']


class Areaf5Serializer(serializers.ModelSerializer):
    product_num = serializers.IntegerField(default=0)
    class Meta:
        model = Shop_data
        fields = ['Areaf5', 'product_num']


class StateSerializer(serializers.ModelSerializer):
    product_num = serializers.IntegerField(default=0)
    class Meta:
        model = Shop_data
        fields = ['State', 'product_num']


class CitySerializer(serializers.ModelSerializer):
    product_num = serializers.IntegerField(default=0)
    class Meta:
        model = Shop_data
        fields = ['City', 'product_num']
        

class HistorySerializer(serializers.ModelSerializer):
    Phone =         serializers.IntegerField(source='Product.Phone')
    Exp_day =       serializers.IntegerField(source='Product.Exp_day')
    Exp_month =     serializers.IntegerField(source='Product.Exp_month')
    Exp_year =      serializers.IntegerField(source='Product.Exp_year')
    Puk_code =      serializers.DecimalField(decimal_places=0, max_digits=8, source='Product.Puk_code')
    First_name =    serializers.CharField(source='Product.First_name')
    Last_name =     serializers.CharField(source='Product.Last_name')
    Address =       serializers.CharField(source='Product.Address')
    City =          serializers.CharField(source='Product.City')
    State =         serializers.CharField(source='Product.State')
    Zipcode =       serializers.CharField(source='Product.Zipcode')
    Extra1 =        serializers.CharField(source='Product.Extra1')
    Extra2 =        serializers.CharField(source='Product.Extra2')
    Extra3 =        serializers.CharField(source='Product.Extra3')
    Extra4 =        serializers.CharField(source='Product.Extra4')
    Extra5 =        serializers.CharField(source='Product.Extra5')
    Areaf1 =        serializers.CharField(source='Product.Areaf1')
    Areaf2 =        serializers.CharField(source='Product.Areaf2')
    Areaf3 =        serializers.CharField(source='Product.Areaf3')
    Areaf4 =        serializers.CharField(source='Product.Areaf4')
    Areaf5 =        serializers.CharField(source='Product.Areaf5')
    Areaf6 =        serializers.CharField(source='Product.Areaf6')
    Area_code =     serializers.DecimalField(decimal_places=0, max_digits=6, source='Product.Area_code')
    Sold_date =     serializers.DateTimeField(source='Product.Sold_date')
    Gender =        serializers.SerializerMethodField()
    Batch_id =      serializers.IntegerField(source='Product.Batch.id')
    Batch_Name =    serializers.CharField(source='Product.Batch.Name')
    Batch_Publish_date = serializers.DateTimeField(source='Product.Batch.Publish_date')
    Item_cost =     serializers.DecimalField(decimal_places=2, max_digits=10, source='Product.Price')
    Checker_cost =  serializers.CharField(source='Checker.Cost')
    Checker_name =  serializers.CharField(source='Checker.Name')
    class Meta:
        model = Order_history
        fields = ['Phone', 'Exp_day', 'Exp_month', 'Exp_year', 'Puk_code', 'First_name', 'Last_name', 'Gender', 'Address', 'City', 'State', 'Zipcode', 'Extra1', 'Extra2', 'Extra3', 'Extra4', 'Extra5', 'Item_cost', 'Areaf1', 'Areaf2', 'Areaf3', 'Areaf4', 'Areaf5', 'Areaf6', 'Area_code', 'Sold_date', 'Batch_id', 'Batch_Name', 'Batch_Publish_date', 'Checker_cost', 'Checker_name', 'Checker_status']

    def get_Gender(self,obj):
        if obj.Product.Gender == 'M':
            return 'Male'
        elif obj.Product.Gender == 'F':
            return 'Female'
        elif obj.Product.Gender == 'M':
            return 'Unknown'