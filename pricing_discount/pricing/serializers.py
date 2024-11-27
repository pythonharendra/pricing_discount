from rest_framework import serializers
from .models import Product, SeasonalProduct, BulkProduct, Discount, PercentageDiscount, FixedAmountDiscount, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'base_price']


class SeasonalProductSerializer(ProductSerializer):
    class Meta:
        model = SeasonalProduct
        fields = ['id', 'name', 'base_price', 'seasonal_discount']


class BulkProductSerializer(ProductSerializer):
    class Meta:
        model = BulkProduct
        fields = ['id', 'name', 'base_price', 'bulk_discount', 'minmun_quantity_for_discount']


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'discount_name', 'start_date', 'end_date', 'is_active']


class PercentageDiscountSerializer(DiscountSerializer):
    class Meta:
        model = PercentageDiscount
        fields = ['id', 'discount_name', 'start_date', 'end_date', 'is_active', 'percentage']


class FixedAmountDiscountSerializer(DiscountSerializer):
    class Meta:
        model = FixedAmountDiscount
        fields = ['id', 'discount_name', 'start_date', 'end_date', 'is_active', 'amount']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    discount = DiscountSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'discount']

    def get_product_price(self):
        return self.product.get_price(self.quantity)

    def apply_discount(self):
        """Apply discount if available."""
        if self.discount and self.discount.is_active:
            return self.discount.apply_discount(self.get_product_price())
        return self.get_product_price()


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_email', 'shipping_address', 'order_status', 'order_date', 'items']

    def calculate_total(self):
        total = 0
        for item in self.items:
            product_price = item['product'].get_price(item['quantity'])
            if item['discount'] and item['discount'].is_active:
                product_price = item['discount'].apply_discount(product_price)
            total += product_price * item['quantity']
        return total
