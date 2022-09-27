from email.policy import default
from rest_framework import serializers
from .models import Shop_data


class ProductSerializer(serializers.ModelSerializer):
    Gender = serializers.SerializerMethodField()
    Batch_id = serializers.IntegerField(source='Batch.id')
    Batch_Name = serializers.CharField(source='Batch.Name')
    Batch_Publish_date = serializers.DateTimeField(source='Batch.Publish_date')

    class Meta:
        model = Shop_data
        fields = '__all__'

    def get_Gender(self,obj):
        return obj.get_Gender_display()


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