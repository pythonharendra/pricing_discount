# pricing_discount
Installation and Setup
Prerequisites:
1.
Python 3.7 or above installed on your machine.
Clone the Repository:

2.
bash
Copy code
https://github.com/pythonharendra/pricing_discount.git
cd order-management-system
Run the Code: Ensure Python is installed and run the script directly:
3.

bash
Copy code
python order_management.py


1. Define Products
Create instances of Product, SeasonalProduct, or BulkProduct as needed:

seasonal_product = SeasonalProduct("Winter Coat", base_price=200, seasonal_discount_percentage=20)
bulk_product = BulkProduct("Notebook", base_price=5, bulk_discount_threshold=10, bulk_discount_percentage=15)


2. Define Discounts
Create instances of PercentageDiscount or FixedAmountDiscount:

percentage_discount = PercentageDiscount(
    name="Holiday Discount",
    description="10% off during holidays",
    start_date=date(2024, 11, 1),
    end_date=date(2024, 12, 31),
    percentage=10
)

fixed_discount = FixedAmountDiscount(
    name="Clearance Sale",
    description="Flat $50 off",
    start_date=date(2024, 10, 1),
    end_date=date(2024, 10, 31),
    fixed_amount=50
)


3. Create an Order:
order = Order(customer_name="John Doe")
order.add_item(seasonal_product, quantity=1, discount=percentage_discount)
order.add_item(bulk_product, quantity=12, discount=fixed_discount)

print("Total Order Price:", order.calculate_total())
