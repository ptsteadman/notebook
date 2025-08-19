"""
You're building a shopping cart pricer app for your local grocery store.

They sell many types of items and accept coupons. One type of coupon discounts an item's price by a percentage (eg. 10% off). 
Another type of coupon gives the shopper a dollar amount discount if a minimum count of the item is purchased (eg. $5 off if you buy 2 or more). 
A shopper may only use one coupon on a type of item.


The app should compute the price, given a shopping cart and a set of coupons applied.
 Keep in mind the grocery store is planning to accept new types of coupons the next quarter, but you don't yet know the details of those.

Given this information, design the interface(s) and data model to represent the shopping cart, implement the shopping cart pricer, and test your code.

As an example, a shopping cart has 10 apples ($1 each), 2 loaves of bread ($5 each), and 1 chocolate ($1 each).

The shopper has two coupons: 10% off for apples and $4 off for buying 2 or more loaves of bread. The pricer should return $16. 

apples: 10 * 1, 10% coupon: $9
bread: 2 * 5: $4 off coupon: $6
chocolate: 1 * 1: $1 
total: $16

Note the extra loaves are not counted in the final undiscounted price.

Write tests for:

Computing the best price of a cart when you have multiple coupons on the same item.
When you remove an item from the cart.
Adding an item with a negative price.
Discuss a broader variety of coupons, like coupons that apply when you have multiple different items with minimum quantities.

Code the cart to assume that the most recent coupon for an item is the one that will be used.
Then change the code to accept all coupons for an item and compute which discount would be the best for the item.
"""

from abc import ABC, abstractmethod
from re import sub
from typing import Dict, List
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
import unittest


@dataclass
class Item:
    """Represents an item in the store with a name and price."""
    name: str
    price: Decimal
    
    def __post_init__(self):
        if self.price < 0:
            raise ValueError(f"Item price cannot be negative: {self.price}")


class Coupon(ABC):
    """Abstract base class for all coupon types."""
    
    @abstractmethod
    def calculate_discount(self, item_name: str, quantity: int, unit_price: Decimal) -> Decimal:
        """Calculate the discount amount for a given item and quantity. Returns 0 if coupon cannot be applied."""
        pass


class PercentageCoupon(Coupon):
    """Coupon that applies a percentage discount to an item."""
    
    def __init__(self, item_name: str, percentage: Decimal):
        self.item_name = item_name
        self.percentage = percentage
        if percentage < 0 or percentage > 100:
            raise ValueError(f"Percentage must be between 0 and 100: {percentage}")
    
    def calculate_discount(self, item_name: str, quantity: int, unit_price: Decimal) -> Decimal:
        if item_name != self.item_name or quantity <= 0:
            return Decimal('0')
        
        total_price = unit_price * quantity
        discount = total_price * (self.percentage / Decimal('100'))
        return discount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


class DollarAmountCoupon(Coupon):
    """Coupon that gives a dollar amount discount if minimum quantity is met."""
    
    def __init__(self, item_name: str, discount_amount: Decimal, min_quantity: int):
        self.item_name = item_name
        self.discount_amount = discount_amount
        self.min_quantity = min_quantity
        
        if discount_amount < 0:
            raise ValueError(f"Discount amount cannot be negative: {discount_amount}")
        if min_quantity < 1:
            raise ValueError(f"Minimum quantity must be at least 1: {min_quantity}")
    
    def calculate_discount(self, item_name: str, quantity: int, unit_price: Decimal) -> Decimal:
        if item_name != self.item_name or quantity < self.min_quantity:
            return Decimal('0')
        
        return self.discount_amount


class ShoppingCart:
    """Represents a shopping cart with items and coupons."""
    
    def __init__(self):
        self.items: Dict[str, int] = {}  # item_name -> quantity
        self.item_prices: Dict[str, Decimal] = {}  # item_name -> unit_price
        self.coupons: Dict[str, List[Coupon]] = {}  # item_name -> list of coupons
    
    def add_item(self, item: Item, quantity: int = 1):
        """Add an item to the cart."""
        if quantity <= 0:
            raise ValueError(f"Quantity must be positive: {quantity}")
        
        if item.name in self.items:
            self.items[item.name] += quantity
        else:
            self.items[item.name] = quantity
            self.item_prices[item.name] = item.price
    
    def add_coupon(self, coupon: Coupon):
        """Add a coupon to the cart."""
        item_name = getattr(coupon, 'item_name', None)
        if not item_name:
            raise ValueError("Coupon must have an item_name attribute")
        
        if item_name not in self.coupons:
            self.coupons[item_name] = []
        self.coupons[item_name].append(coupon)
    
    def _get_best_coupon_discount(self, item_name: str, quantity: int, unit_price: Decimal) -> Decimal:
        """Find the best discount among all coupons for an item."""
        if item_name not in self.coupons:
            return Decimal('0')
        
        best_discount = Decimal('0')
        for coupon in self.coupons[item_name]:
            discount = coupon.calculate_discount(item_name, quantity, unit_price)
            if discount > best_discount:
                best_discount = discount
        
        return best_discount
    
    def calculate_total(self) -> Decimal:
        """Calculate the total price of the cart with all applicable discounts."""
        subtotal = Decimal('0')
        discounts = Decimal('0')
        
        # Calculate subtotal and item-specific discounts
        for item_name, quantity in self.items.items():
            unit_price = self.item_prices[item_name]
            item_total = unit_price * quantity
            subtotal += item_total
            
            # Apply best coupon discount for this item
            item_discount = self._get_best_coupon_discount(item_name, quantity, unit_price)
            discounts += item_discount
        
        total = subtotal - discounts
        return max(total, Decimal('0'))  # Total cannot be negative

class MyCoupon(ABC):
    @abstractmethod
    def calculate_discount(self, MyShoppingCart) -> Decimal:
        pass


class PercentageCoupon(MyCoupon):
    def __init__(self, item_name: str, percent_off: int):
        self.item_name = item_name
        self.percent_off = percent_off

    def calculate_discount(self, cart: MyShoppingCart) -> Decimal:
        if self.item_name not in cart.items:
            return Decimal('0')
        
        subtotal = cart.catalog[self.item_name] * cart.items[self.item_name]
        discount = subtotal * (self.percent_off / 100)
        return discount



class MyShoppingCart:
    def __init__(self):
        self.catalog: Dict[str, Decimal] = {}
        self.items: Dict[str, int] = collections.defaultdict(int)
        self.coupons: Dict[str, MyCoupon] = {}

    def add_item(self, item: Item, quantity: int):
        if item.name not in self.catalog:
            self.catalog[item.name] = item.price
        self.items[item.name] += quantity

    def add_coupon(self, coupon)


# Test cases
class TestShoppingCart(unittest.TestCase):
    
    def setUp(self):
        self.cart = ShoppingCart()
        self.apple = Item("apple", Decimal('1.00'))
        self.bread = Item("bread", Decimal('5.00'))
        self.chocolate = Item("chocolate", Decimal('1.00'))
    
    def test_basic_example(self):
        """Test the basic example from the problem description."""
        # Add items
        self.cart.add_item(self.apple, 10)
        self.cart.add_item(self.bread, 2)
        self.cart.add_item(self.chocolate, 1)
        
        # Add coupons
        apple_coupon = PercentageCoupon("apple", Decimal('10'))
        bread_coupon = DollarAmountCoupon("bread", Decimal('4.00'), 2)
        
        self.cart.add_coupon(apple_coupon)
        self.cart.add_coupon(bread_coupon)
        
        # Expected: apples: 10 * 1 - 10% = 9, bread: 2 * 5 - 4 = 6, chocolate: 1 = 1, total: 16
        self.assertEqual(self.cart.calculate_total(), Decimal('16.00'))
    
    def test_multiple_coupons_same_item(self):
        """Test when multiple coupons are available for the same item."""
        self.cart.add_item(self.apple, 5)
        
        # Add two different coupons for apples
        coupon1 = PercentageCoupon("apple", Decimal('20'))  # 20% off
        coupon2 = DollarAmountCoupon("apple", Decimal('2.00'), 3)  # $2 off if buy 3+
        
        self.cart.add_coupon(coupon1)
        self.cart.add_coupon(coupon2)
        
        # 20% off: 5 * 1 * 0.2 = 1.00 discount
        # $2 off: 2.00 discount
        # Should choose the better discount ($2 off)
        self.assertEqual(self.cart.calculate_total(), Decimal('3.00'))  # 5 - 2 = 3
    
    def test_negative_price_item(self):
        """Test adding an item with negative price (should raise error)."""
        with self.assertRaises(ValueError):
            negative_item = Item("negative_item", Decimal('-1.00'))
    
    def test_coupon_validation(self):
        """Test coupon validation."""
        # Test invalid percentage
        with self.assertRaises(ValueError):
            PercentageCoupon("apple", Decimal('150'))
        
        # Test negative discount amount
        with self.assertRaises(ValueError):
            DollarAmountCoupon("bread", Decimal('-1.00'), 2)
        
        # Test invalid minimum quantity
        with self.assertRaises(ValueError):
            DollarAmountCoupon("bread", Decimal('1.00'), 0)
    
    def test_empty_cart(self):
        """Test empty cart total."""
        self.assertEqual(self.cart.calculate_total(), Decimal('0.00'))
    
    def test_coupon_returns_zero_when_not_applicable(self):
        """Test that coupons return 0 when they cannot be applied."""
        # Test percentage coupon for wrong item
        apple_coupon = PercentageCoupon("apple", Decimal('10'))
        self.assertEqual(apple_coupon.calculate_discount("bread", 5, Decimal('1.00')), Decimal('0'))
        
        # Test percentage coupon for zero quantity
        self.assertEqual(apple_coupon.calculate_discount("apple", 0, Decimal('1.00')), Decimal('0'))
        
        # Test dollar amount coupon for insufficient quantity
        bread_coupon = DollarAmountCoupon("bread", Decimal('2.00'), 3)
        self.assertEqual(bread_coupon.calculate_discount("bread", 2, Decimal('5.00')), Decimal('0'))
        
        # Test dollar amount coupon for wrong item
        self.assertEqual(bread_coupon.calculate_discount("apple", 5, Decimal('1.00')), Decimal('0'))


if __name__ == "__main__":
    # Run the example from the problem description
    print("Running example from problem description:")
    cart = ShoppingCart()
    
    # Add items
    apple = Item("apple", Decimal('1.00'))
    bread = Item("bread", Decimal('5.00'))
    chocolate = Item("chocolate", Decimal('1.00'))
    
    cart.add_item(apple, 10)
    cart.add_item(bread, 2)
    cart.add_item(chocolate, 1)
    
    # Add coupons
    apple_coupon = PercentageCoupon("apple", Decimal('10'))
    bread_coupon = DollarAmountCoupon("bread", Decimal('4.00'), 2)
    
    cart.add_coupon(apple_coupon)
    cart.add_coupon(bread_coupon)
    
    total = cart.calculate_total()
    print(f"Total: ${total}")
    
    # Run tests
    print("\nRunning tests:")
    unittest.main(argv=[''], exit=False, verbosity=2)
