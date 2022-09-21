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
    class Meta:
        model = Shop_data
        fields = ['Areaf1']


class Areaf2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Shop_data
        fields = ['Areaf2']


class Areaf3Serializer(serializers.ModelSerializer):
    class Meta:
        model = Shop_data
        fields = ['Areaf3']


class Areaf4Serializer(serializers.ModelSerializer):
    class Meta:
        model = Shop_data
        fields = ['Areaf4']


class Areaf5Serializer(serializers.ModelSerializer):
    class Meta:
        model = Shop_data
        fields = ['Areaf5']


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop_data
        fields = ['State']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop_data
        fields = ['City']