"""
Design and implement a cache layer. 
There will be a config to switch between different cache policies, like LRU and LFU. 
Also, clean up the data older than one day.
"""

import time
import threading
import unittest
from collections import defaultdict
from typing import Any, Optional, Dict, List, Tuple


# ----------------------------
# Policy Interfaces & Classes
# ----------------------------

class BasePolicy:
    """Interface for cache eviction policies."""

    def get(self, key: str) -> Optional[Any]:
        raise NotImplementedError

    def put(self, key: str, value: Any, capacity: int) -> List[str]:
        """Insert/update key. Return list of evicted keys (at most one)."""
        raise NotImplementedError

    def remove(self, key: str) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError

    def contains(self, key: str) -> bool:
        raise NotImplementedError

    def size(self) -> int:
        raise NotImplementedError


class LRUPolicy(BasePolicy):
    """LRU policy using standard dict insertion order.

    - Most recently used keys are moved to the end by re-inserting (pop and set).
    - Eviction removes the least recently used key (first key in dict order).
    """

    def __init__(self) -> None:
        self._store: Dict[str, Any] = {}

    def _move_to_end(self, key: str) -> None:
        if key in self._store:
            value = self._store.pop(key)
            self._store[key] = value

    def get(self, key: str) -> Optional[Any]:
        if key not in self._store:
            return None
        value = self._store[key]
        self._move_to_end(key)
        return value

    def put(self, key: str, value: Any, capacity: int) -> List[str]:
        evicted: List[str] = []
        if key in self._store:
            # Update value and mark as most recently used
            self._store.pop(key)
            self._store[key] = value
            return evicted

        # Insert new key. Evict if needed.
        if capacity <= 0:
            return evicted

        if len(self._store) >= capacity:
            # Evict least recently used (the first key)
            oldest_key = next(iter(self._store))
            evicted.append(oldest_key)
            del self._store[oldest_key]
        self._store[key] = value
        return evicted

    def remove(self, key: str) -> None:
        if key in self._store:
            del self._store[key]

    def clear(self) -> None:
        self._store.clear()

    def contains(self, key: str) -> bool:
        return key in self._store

    def size(self) -> int:
        return len(self._store)


class LFUPolicy(BasePolicy):
    """LFU policy using the two-map solution with standard dicts.

    Structures:
      - _values: key -> value
      - _key_freq: key -> current frequency
      - _freq_to_keys: freq -> dict of keys (values unused, using dict for insertion order)
      - _min_freq: smallest frequency among keys (for O(1) eviction)
    """

    def __init__(self) -> None:
        self._values: Dict[str, Any] = {}
        self._key_freq: Dict[str, int] = {}
        self._freq_to_keys: Dict[int, Dict[str, None]] = defaultdict(dict)
        self._min_freq: int = 0

    def _touch(self, key: str) -> None:
        """Increase key frequency and move it to the new bucket."""
        freq = self._key_freq[key]
        # Remove from old bucket
        bucket = self._freq_to_keys[freq]
        if key in bucket:
            del bucket[key]
        if not bucket:
            del self._freq_to_keys[freq]
            if self._min_freq == freq:
                # Increase min_freq until we find an existing bucket (if any)
                self._min_freq += 1
                while self._min_freq in self._freq_to_keys and not self._freq_to_keys[self._min_freq]:
                    del self._freq_to_keys[self._min_freq]
                    self._min_freq += 1
        # Add to new bucket
        new_freq = freq + 1
        self._key_freq[key] = new_freq
        self._freq_to_keys[new_freq][key] = None

    def get(self, key: str) -> Optional[Any]:
        if key not in self._values:
            return None
        value = self._values[key]
        self._touch(key)
        return value

    def put(self, key: str, value: Any, capacity: int) -> List[str]:
        evicted: List[str] = []
        if capacity <= 0:
            return evicted

        if key in self._values:
            # Update value and treat as access (increase frequency)
            self._values[key] = value
            self._touch(key)
            return evicted

        # Evict if at capacity
        if len(self._values) >= capacity:
            # Evict the least frequently used key, tie-broken by insertion order within the bucket
            freq = self._min_freq
            bucket = self._freq_to_keys[freq]
            evict_key = next(iter(bucket))
            del bucket[evict_key]
            if not bucket:
                del self._freq_to_keys[freq]
            del self._values[evict_key]
            del self._key_freq[evict_key]
            evicted.append(evict_key)

        # Insert new key with frequency 1
        self._values[key] = value
        self._key_freq[key] = 1
        self._freq_to_keys[1][key] = None
        self._min_freq = 1
        return evicted

    def remove(self, key: str) -> None:
        if key not in self._values:
            return
        freq = self._key_freq[key]
        del self._values[key]
        del self._key_freq[key]
        bucket = self._freq_to_keys.get(freq)
        if bucket and key in bucket:
            del bucket[key]
            if not bucket:
                del self._freq_to_keys[freq]
                if self._min_freq == freq:
                    # Try to advance min_freq to the next existing bucket if any
                    while self._min_freq in self._freq_to_keys and not self._freq_to_keys[self._min_freq]:
                        del self._freq_to_keys[self._min_freq]
                        self._min_freq += 1

    def clear(self) -> None:
        self._values.clear()
        self._key_freq.clear()
        self._freq_to_keys.clear()
        self._min_freq = 0

    def contains(self, key: str) -> bool:
        return key in self._values

    def size(self) -> int:
        return len(self._values)


# --------------
# Cache Facade
# --------------

class Cache:
    def __init__(self, policy: str = "LRU", size: int = 100, ttl_days: float = 1.0, cleanup_interval_seconds: float = 60.0):
        """
        Initialize cache with specified policy and size.
        
        Args:
            policy: "LRU" or "LFU"
            size: Maximum number of items in cache
            ttl_days: Time to live in days (default 1 day)
            cleanup_interval_seconds: Background cleanup interval
        """
        if policy not in {"LFU", "LRU"}:
            raise ValueError("Invalid cache policy. Must be 'LRU' or 'LFU'.")

        self.size_limit = size
        self.ttl_seconds = ttl_days * 24 * 60 * 60
        self.timestamps: Dict[str, float] = {}
        self._lock = threading.RLock()

        if policy == "LRU":
            self._policy: BasePolicy = LRUPolicy()
        else:
            self._policy = LFUPolicy()

        # Start async cleaner
        self._stop_event = threading.Event()
        self._cleanup_interval_seconds = cleanup_interval_seconds
        self._cleaner_thread = threading.Thread(target=self._cleaner_loop, daemon=True)
        self._cleaner_thread.start()

    # ----------- Internal helpers -----------

    def _is_expired_unlocked(self, key: str, now: Optional[float] = None) -> bool:
        ts = self.timestamps.get(key)
        if ts is None:
            return False
        if now is None:
            now = time.time()
        return now - ts > self.ttl_seconds

    def _remove_key_unlocked(self, key: str) -> None:
        self._policy.remove(key)
        if key in self.timestamps:
            del self.timestamps[key]

    def _cleaner_loop(self) -> None:
        while not self._stop_event.is_set():
            self._cleanup_expired_all()
            # Wait with ability to be interrupted
            self._stop_event.wait(self._cleanup_interval_seconds)

    def _cleanup_expired_all(self) -> None:
        now = time.time()
        with self._lock:
            expired_keys = [k for k, ts in list(self.timestamps.items()) if now - ts > self.ttl_seconds]
            for k in expired_keys:
                self._remove_key_unlocked(k)

    # -------------- Public API --------------

    def get(self, key: str) -> Optional[Any]:
        """
        Get value for key. Does not trigger global cleanup, but validates TTL for this key.
        """
        with self._lock:
            # TTL check for this key only
            if self._is_expired_unlocked(key):
                self._remove_key_unlocked(key)
                return None
            value = self._policy.get(key)
            if value is not None:
                # Update access timestamp
                self.timestamps[key] = time.time()
            return value

    def put(self, key: str, value: Any) -> None:
        with self._lock:
            evicted_keys = self._policy.put(key, value, self.size_limit)
            # Remove timestamps for evicted keys
            for k in evicted_keys:
                if k in self.timestamps:
                    del self.timestamps[k]
            # Update timestamp for this key
            self.timestamps[key] = time.time()

    def clear(self) -> None:
        with self._lock:
            self._policy.clear()
            self.timestamps.clear()

    def size(self) -> int:
        with self._lock:
            return self._policy.size()

    def contains(self, key: str) -> bool:
        with self._lock:
            if key not in self.timestamps:
                return False
            if self._is_expired_unlocked(key):
                # Optional: eagerly drop if expired
                self._remove_key_unlocked(key)
                return False
            return self._policy.contains(key)

    # For graceful shutdown (optional)
    def stop(self) -> None:
        self._stop_event.set()
        # Don't join daemon thread on interpreter shutdown
        if self._cleaner_thread.is_alive():
            self._cleaner_thread.join(timeout=0.1)


# --------------
# Tests
# --------------

class Tester(unittest.TestCase):
    def test_LRU(self):
        """Test LRU cache functionality."""
        cache = Cache("LRU", size=3, cleanup_interval_seconds=0.01)
        
        # Test basic put/get
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)
        
        # Test LRU eviction
        cache.put("d", 4)  # Should evict "a" (least recently used)
        self.assertIsNone(cache.get("a"))
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)
        self.assertEqual(cache.get("d"), 4)
        
        # Test access updates LRU order
        cache.get("b")  # Make "b" most recently used
        cache.put("e", 5)  # Should evict "c" (least recently used)
        self.assertIsNone(cache.get("c"))
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("d"), 4)
        self.assertEqual(cache.get("e"), 5)

    def test_LFU(self):
        """Test LFU cache functionality."""
        cache = Cache("LFU", size=3, cleanup_interval_seconds=0.01)
        
        # Test basic put/get
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)
        
        # Test LFU eviction
        cache.get("a")  # a: freq=2
        cache.get("a")  # a: freq=3
        cache.get("b")  # b: freq=2
        cache.get("c")  # c: freq=2
        
        cache.put("d", 4)  # Should evict "b" or "c" (least frequently used)
        
        # "a" should still be there (highest frequency)
        self.assertEqual(cache.get("a"), 1)
        
        # One of "b" or "c" should be evicted
        b_exists = cache.get("b") is not None
        c_exists = cache.get("c") is not None
        self.assertTrue(b_exists or c_exists)  # At least one should exist
        self.assertFalse(b_exists and c_exists)  # Not both should exist
        
        self.assertEqual(cache.get("d"), 4)

    def test_expiration(self):
        """Test expiration functionality (no per-get cleanup, async cleaner)."""
        cache = Cache("LRU", size=10, ttl_days=0.000001, cleanup_interval_seconds=0.01)  # ~0.086s TTL
        
        cache.put("a", 1)
        self.assertEqual(cache.get("a"), 1)
        
        # Wait for expiration; get() should check and drop it even if cleaner hasn't run
        time.sleep(0.1)
        self.assertIsNone(cache.get("a"))

    def test_invalid_policy(self):
        """Test invalid policy raises exception."""
        with self.assertRaises(ValueError):
            Cache("INVALID", size=10)
    
    def test_clear(self):
        """Test cache clearing."""
        cache = Cache("LRU", size=10)
        cache.put("a", 1)
        cache.put("b", 2)
        
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("b"), 2)
        
        cache.clear()
        
        self.assertIsNone(cache.get("a"))
        self.assertIsNone(cache.get("b"))
    
    def test_contains(self):
        """Test contains method with TTL validation."""
        cache = Cache("LRU", size=10, ttl_days=1.0)
        
        cache.put("a", 1)
        self.assertTrue(cache.contains("a"))
        self.assertFalse(cache.contains("b"))


if __name__ == '__main__':
    unittest.main()