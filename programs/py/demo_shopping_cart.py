#!/usr/bin/env python3
"""
Demonstration script for the Shopping Cart Pricer
"""

from decimal import Decimal
from shopping_cart_pricer import (
    ShoppingCart, Item, PercentageCoupon, 
    DollarAmountCoupon
)


def demo_basic_example():
    """Demonstrate the basic example from the problem description."""
    print("=== Basic Example ===")
    print("Cart: 10 apples ($1 each), 2 bread ($5 each), 1 chocolate ($1 each)")
    print("Coupons: 10% off apples, $4 off if buy 2+ bread")
    
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
    print()


def demo_multiple_coupons():
    """Demonstrate multiple coupons for the same item."""
    print("=== Multiple Coupons for Same Item ===")
    print("Cart: 5 apples ($1 each)")
    print("Coupons: 20% off apples, $2 off if buy 3+ apples")
    
    cart = ShoppingCart()
    
    apple = Item("apple", Decimal('1.00'))
    cart.add_item(apple, 5)
    
    # Add two different coupons for apples
    coupon1 = PercentageCoupon("apple", Decimal('20'))  # 20% off
    coupon2 = DollarAmountCoupon("apple", Decimal('2.00'), 3)  # $2 off if buy 3+
    
    cart.add_coupon(coupon1)
    cart.add_coupon(coupon2)
    
    total = cart.calculate_total()
    print(f"Total: ${total}")
    print("(Should choose the better discount: $2 off instead of 20% off)")
    print()


def demo_complex_scenario():
    """Demonstrate a more complex scenario with multiple types of coupons."""
    print("=== Complex Scenario ===")
    print("Cart: 8 apples ($1 each), 3 bread ($5 each), 2 chocolate ($1 each)")
    print("Coupons:")
    print("- 15% off apples")
    print("- $2 off if buy 3+ bread")
    
    cart = ShoppingCart()
    
    apple = Item("apple", Decimal('1.00'))
    bread = Item("bread", Decimal('5.00'))
    chocolate = Item("chocolate", Decimal('1.00'))
    
    cart.add_item(apple, 8)
    cart.add_item(bread, 3)
    cart.add_item(chocolate, 2)
    
    # Add multiple coupons
    apple_coupon = PercentageCoupon("apple", Decimal('15'))
    bread_coupon = DollarAmountCoupon("bread", Decimal('2.00'), 3)
    
    cart.add_coupon(apple_coupon)
    cart.add_coupon(bread_coupon)
    
    total = cart.calculate_total()
    print(f"Total: ${total}")
    print("(8 + 3*5 + 2 - 1.20 - 2 = 21.80)")
    print()


if __name__ == "__main__":
    print("Shopping Cart Pricer Demonstration\n")
    
    demo_basic_example()
    demo_multiple_coupons()
    demo_complex_scenario()
    
    print("All demonstrations completed!")
