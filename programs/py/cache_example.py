#!/usr/bin/env python3
"""
Example usage of the Cache class demonstrating LRU and LFU policies.
"""

from cache import Cache
import time

def demo_lru_cache():
    """Demonstrate LRU cache behavior."""
    print("=== LRU Cache Demo ===")
    cache = Cache("LRU", size=3)
    
    # Add items
    cache.put("apple", "red fruit")
    cache.put("banana", "yellow fruit")
    cache.put("cherry", "red berry")
    
    print(f"Cache contains 'apple': {cache.contains('apple')}")
    print(f"Cache contains 'banana': {cache.contains('banana')}")
    print(f"Cache contains 'cherry': {cache.contains('cherry')}")
    
    # Access 'apple' to make it most recently used
    print(f"Getting 'apple': {cache.get('apple')}")
    
    # Add new item - should evict 'banana' (least recently used)
    cache.put("date", "sweet fruit")
    
    print(f"After adding 'date':")
    print(f"  'apple': {cache.get('apple')} (should exist)")
    print(f"  'banana': {cache.get('banana')} (should be None)")
    print(f"  'cherry': {cache.get('cherry')} (should exist)")
    print(f"  'date': {cache.get('date')} (should exist)")

def demo_lfu_cache():
    """Demonstrate LFU cache behavior."""
    print("\n=== LFU Cache Demo ===")
    cache = Cache("LFU", size=3)
    
    # Add items
    cache.put("a", "first")
    cache.put("b", "second")
    cache.put("c", "third")
    
    # Access 'a' multiple times to increase its frequency
    cache.get("a")  # freq = 2
    cache.get("a")  # freq = 3
    cache.get("a")  # freq = 4
    
    # Access 'b' once
    cache.get("b")  # freq = 2
    
    # Access 'c' once
    cache.get("c")  # freq = 2
    
    print(f"After accessing items:")
    print(f"  'a' frequency: 4 (highest)")
    print(f"  'b' frequency: 2")
    print(f"  'c' frequency: 2")
    
    # Add new item - should evict 'b' or 'c' (lowest frequency)
    cache.put("d", "fourth")
    
    print(f"After adding 'd':")
    print(f"  'a': {cache.get('a')} (should exist - highest frequency)")
    print(f"  'b': {cache.get('b')} (might be evicted)")
    print(f"  'c': {cache.get('c')} (might be evicted)")
    print(f"  'd': {cache.get('d')} (should exist)")

def demo_expiration():
    """Demonstrate expiration functionality."""
    print("\n=== Expiration Demo ===")
    cache = Cache("LRU", size=10, ttl_days=0.000001)  # Very short TTL (about 0.086 seconds)
    
    cache.put("temp", "temporary data")
    print(f"Immediately after put: {cache.get('temp')}")
    
    time.sleep(0.1)  # Wait for expiration
    
    print(f"After waiting: {cache.get('temp')} (should be None)")

if __name__ == "__main__":
    demo_lru_cache()
    demo_lfu_cache()
    demo_expiration()
