from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('status', 'yoco_checkout_id', 'yoco_payment_id', 'created_at', 'updated_at')
