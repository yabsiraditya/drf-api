from rest_framework import serializers
from .models import User, Product, Order, Purchase


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'stock',
        ]

        def validate_price(self, value):
            if value <= 0:
                raise serializers.ValidationError(
                    "Harga tidak boleh kosong"
                )
            return value