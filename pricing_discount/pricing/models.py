
from datetime import date,datetime

import uuid



class Product:
    """
    this  base class of product with a base price.

    Attributes:
        name : Name of the product.
        base_price: Base price of the product.
    """
    def __init__(self, name, base_price):
        self.name = name
        self.base_price = base_price

    def get_price(self):
        return self.base_price
    

class SeasonalProduct(Product):

    ''' product with seasonal discounts, it inherit product class.
    '''
    def __init__(self, name, base_price, seasonal_discount_percentage):
        super().__init__(name, base_price)
        self.seasonal_discount_percentage = seasonal_discount_percentage

    def get_price(self):
        '''Calculate the price after applying the seasonal discount.'''

        return self.base_price * (1 - self.seasonal_discount_percentage / 100)


class BulkProduct(Product):
    ''' product with seasonal discounts, it inherit product class.
    '''
    def __init__(self, name, base_price, bulk_discount_threshold, bulk_discount_percentage):
        super().__init__(name, base_price)
        self.bulk_discount_threshold = bulk_discount_threshold
        self.bulk_discount_percentage = bulk_discount_percentage

    def get_price(self, quantity=1):

        '''Calculate the price after applying the bulk discount.'''

        if quantity >= self.bulk_discount_threshold:
            return self.base_price * (1 - self.bulk_discount_percentage / 100)
        return self.base_price
    


class Discount:
    ''' base class of discount . it has the basic info about all discounts'''
    def __init__(self, name, description, start_date, end_date):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date

    def is_valid(self):
        """Check if the discount is valid on the current date."""
        today = date.today()
        return self.start_date <= today <= self.end_date

    def apply_discount(self, price):
        raise NotImplementedError("This method should be overridden by subclasses.")


class PercentageDiscount(Discount):

    ''' this is percentage-based discount.'''
    def __init__(self, name, description, start_date, end_date, percentage):
        super().__init__(name, description, start_date, end_date)
        self.percentage = percentage

    def apply_discount(self, price):
        '''Apply the percentage discount to the given price.'''
        if self.is_valid():
            return price * (1 - self.percentage / 100)
        return price


class FixedAmountDiscount(Discount):
    ''' this is fixed amount-based discount. apply when threshold hit'''
    def __init__(self, name, description, start_date, end_date, fixed_amount):
        super().__init__(name, description, start_date, end_date)
        self.fixed_amount = fixed_amount

    def apply_discount(self, price):
        if self.is_valid():
            return max(price - self.fixed_amount, 0)
        return price






class Order:
    '''base class of order . it has basic details of every order'''
    def __init__(self, customer_name):
        self.order_id = str(uuid.uuid4())  # Unique order ID
        self.customer_name = customer_name
        self.order_date = datetime.now()
        self.items = []  # List of products in the order

    def add_item(self, product, quantity, discount=None):
        """Add a product with quantity and optional discount to the order."""
        self.items.append({
            "product": product,
            "quantity": quantity,
            "discount": discount,
        })

    def calculate_total(self):
        """Calculate the total price of the order."""
        total = 0
        for item in self.items:
            # Calculate product price
            if isinstance(item["product"], BulkProduct):
                price = item["product"].get_price(item["quantity"])
            else:
                price = item["product"].get_price()

            # Apply discount if available
            if item["discount"] and item["discount"].is_valid():
                price = item["discount"].apply_discount(price)

            # Add to total
            total += price * item["quantity"]
        return total

   
 


