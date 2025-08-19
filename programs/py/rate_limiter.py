"""
We want to protect an API endpoint with an in-memory rate limiter.

The rate limiter should be initialized with a value that represents the maximum requests per second we want to allow.

When a request hits the API endpoint, the rate limiter is asked whether it has capacity to process this request and will reject or accept the request appropriately.

Assume:

Time is measured in millisecond resolution.
API requests come in sequentially.
Design the interface and implement the logic for the rate limiter.

Example at a max of 2 requests / sec:

12:00:01.100 PASS
12:00:01.200 PASS
12:00:01.300 FAIL
12:00:02.100 PASS
12:00:02.150 FAIL
12:00:02.200 PASS
"""

import collections
import time
from typing import Optional, Callable
import unittest


class Clock:
    """Abstract clock interface for getting current time."""
    
    def get_current_time_ms(self) -> int:
        """Get current time in milliseconds."""
        return int(time.time() * 1000)


class MockClock:
    """Mock clock for testing with controlled time."""
    
    def __init__(self, initial_time_ms: int = 0):
        self.current_time_ms = initial_time_ms
    
    def get_current_time_ms(self) -> int:
        """Get the current mock time in milliseconds."""
        return self.current_time_ms
    
    def advance(self, milliseconds: int):
        """Advance the mock time by the specified milliseconds."""
        self.current_time_ms += milliseconds
    
    def set_time(self, milliseconds: int):
        """Set the mock time to the specified milliseconds."""
        self.current_time_ms = milliseconds


class CustomClock(Clock):
    """Example of a custom clock implementation."""
    
    def __init__(self, time_offset_ms: int = 0):
        self.time_offset_ms = time_offset_ms
    
    def get_current_time_ms(self) -> int:
        """Get current time with offset."""
        return int(time.time() * 1000) + self.time_offset_ms


class RateLimiter:
    def __init__(self, max_rps: int, clock: Optional[Clock] = None):
        """
        Initialize the rate limiter with maximum requests per second.
        
        Args:
            max_rps: Maximum requests allowed per second
            clock: Clock instance for getting current time. If None, uses system clock.
        """
        self.max_rps = max_rps
        self.requests = collections.deque()  # Store timestamps of recent requests
        self.window_size = 1000  # 1 second in milliseconds
        self.clock = clock or Clock()
    
    def is_allowed(self, current_time_ms: Optional[int] = None) -> bool:
        """
        Check if a new request is allowed based on the rate limit.
        
        Args:
            current_time_ms: Current time in milliseconds. If None, uses clock.
            
        Returns:
            True if request is allowed, False otherwise
        """
        if current_time_ms is None:
            current_time_ms = self.clock.get_current_time_ms()
        
        # Remove requests older than 1 second
        while self.requests and current_time_ms - self.requests[0] >= self.window_size:
            self.requests.popleft()
        
        # Check if we have capacity for a new request
        if len(self.requests) < self.max_rps:
            self.requests.append(current_time_ms)
            return True
        
        return False
    
    def get_current_count(self, current_time_ms: Optional[int] = None) -> int:
        """
        Get the current number of requests in the sliding window.
        
        Args:
            current_time_ms: Current time in milliseconds. If None, uses clock.
            
        Returns:
            Number of requests in the current window
        """
        if current_time_ms is None:
            current_time_ms = self.clock.get_current_time_ms()
        
        # Remove old requests
        while self.requests and current_time_ms - self.requests[0] >= self.window_size:
            self.requests.popleft()
        
        return len(self.requests)


# Example usage and testing
class TestRateLimiter(unittest.TestCase):
    """Test cases for the RateLimiter class."""
    
    def test_basic_rate_limiting(self):
        """Test basic rate limiting functionality with the example scenario."""
        limiter = RateLimiter(max_rps=2)
        
        # Test cases: (timestamp_ms, expected_result)
        test_cases = [
            (100, True),   # 12:00:01.100 PASS
            (200, True),   # 12:00:01.200 PASS  
            (300, False),  # 12:00:01.300 FAIL
            (1100, True),  # 12:00:02.100 PASS
            (1150, False), # 12:00:02.150 FAIL
            (1200, True),  # 12:00:02.200 PASS
        ]
        
        for timestamp, expected in test_cases:
            with self.subTest(timestamp=timestamp):
                result = limiter.is_allowed(timestamp)
                self.assertEqual(result, expected, 
                               f"Expected {expected} for timestamp {timestamp}, got {result}")
    
    def test_rate_limiter_with_different_limits(self):
        """Test rate limiter with different max_rps values."""
        # Test with 1 request per second
        limiter = RateLimiter(max_rps=1)
        self.assertTrue(limiter.is_allowed(100))
        self.assertFalse(limiter.is_allowed(200))
        self.assertTrue(limiter.is_allowed(1100))  # New second
        
        # Test with 3 requests per second
        limiter = RateLimiter(max_rps=3)
        self.assertTrue(limiter.is_allowed(100))
        self.assertTrue(limiter.is_allowed(200))
        self.assertTrue(limiter.is_allowed(300))
        self.assertFalse(limiter.is_allowed(400))
    
    def test_current_time_usage(self):
        """Test that rate limiter works with current system time."""
        limiter = RateLimiter(max_rps=1)
        
        # First request should be allowed
        self.assertTrue(limiter.is_allowed())
        
        # Second request should be denied (within same second)
        self.assertFalse(limiter.is_allowed())
    
    def test_get_current_count(self):
        """Test the get_current_count method."""
        limiter = RateLimiter(max_rps=5)
        
        # Initially should be 0
        self.assertEqual(limiter.get_current_count(100), 0)
        
        # Add some requests with specific timestamps
        limiter.is_allowed(100)
        self.assertEqual(limiter.get_current_count(150), 1)
        
        limiter.is_allowed(200)
        self.assertEqual(limiter.get_current_count(250), 2)
        
        # Test that old requests are cleaned up
        limiter.is_allowed(2000)  # 2 seconds later
        self.assertEqual(limiter.get_current_count(2100), 1)  # Only the latest request remains
    
    def test_rate_limiter_with_mock_clock(self):
        """Test rate limiter using MockClock dependency injection."""
        # Create a mock clock starting at 1000ms
        mock_clock = MockClock(initial_time_ms=1000)
        limiter = RateLimiter(max_rps=2, clock=mock_clock)
        
        # Test requests using mock clock
        self.assertTrue(limiter.is_allowed())   # 1000ms - PASS
        self.assertTrue(limiter.is_allowed())   # 1000ms - PASS
        self.assertFalse(limiter.is_allowed())  # 1000ms - FAIL (limit reached)
        
        # Advance time to new second
        mock_clock.advance(1000)  # Now at 2000ms
        self.assertTrue(limiter.is_allowed())   # 2000ms - PASS (new second)
        self.assertTrue(limiter.is_allowed())   # 2000ms - PASS
        self.assertFalse(limiter.is_allowed())  # 2000ms - FAIL (limit reached)
    
    def test_mock_clock_with_advance_time(self):
        """Test MockClock with time advancement."""
        mock_clock = MockClock(initial_time_ms=1000)
        limiter = RateLimiter(max_rps=1, clock=mock_clock)
        
        # First request
        self.assertTrue(limiter.is_allowed())   # 1000ms - PASS
        self.assertFalse(limiter.is_allowed())  # 1000ms - FAIL
        
        # Advance time by 500ms (still in same second)
        mock_clock.advance(500)
        self.assertFalse(limiter.is_allowed())  # 1500ms - FAIL (same second)
        
        # Advance time by another 600ms (new second)
        mock_clock.advance(600)
        self.assertTrue(limiter.is_allowed())   # 2100ms - PASS (new second)
    
    def test_mock_clock_with_set_time(self):
        """Test MockClock with set_time method."""
        mock_clock = MockClock(initial_time_ms=1000)
        limiter = RateLimiter(max_rps=2, clock=mock_clock)
        
        # Add some requests
        self.assertTrue(limiter.is_allowed())   # 1000ms - PASS
        self.assertTrue(limiter.is_allowed())   # 1000ms - PASS
        
        # Jump to a new time window
        mock_clock.set_time(3000)  # 3 seconds later
        self.assertTrue(limiter.is_allowed())   # 3000ms - PASS (new window)
        self.assertEqual(limiter.get_current_count(), 1)  # Only the new request
    
    def test_mock_clock_edge_cases(self):
        """Test edge cases with MockClock."""
        mock_clock = MockClock(initial_time_ms=1000)
        limiter = RateLimiter(max_rps=1, clock=mock_clock)
        
        # Test exactly at the boundary
        self.assertTrue(limiter.is_allowed())   # 1000ms - PASS
        
        # Just before the window expires
        mock_clock.set_time(1999)
        self.assertFalse(limiter.is_allowed())  # 1999ms - FAIL (same second)
        
        # Exactly at the window boundary
        mock_clock.set_time(2000)
        self.assertTrue(limiter.is_allowed())   # 2000ms - PASS (new second)
        
        # Just after the window boundary
        mock_clock.set_time(2001)
        self.assertFalse(limiter.is_allowed())  # 2001ms - FAIL (same second)
    
    def test_mock_clock_cleanup(self):
        """Test that old requests are properly cleaned up with MockClock."""
        mock_clock = MockClock(initial_time_ms=1000)
        limiter = RateLimiter(max_rps=5, clock=mock_clock)
        
        # Add several requests
        for i in range(3):
            self.assertTrue(limiter.is_allowed())
        
        # Check count
        self.assertEqual(limiter.get_current_count(), 3)
        
        # Advance time to expire all requests
        mock_clock.advance(2000)  # 2 seconds later
        
        # All requests should be cleaned up
        self.assertEqual(limiter.get_current_count(), 0)
        
        # New request should be allowed
        self.assertTrue(limiter.is_allowed())
        self.assertEqual(limiter.get_current_count(), 1)
    
    def test_custom_clock_implementation(self):
        """Test using a custom clock implementation."""
        # Create a custom clock with a 5-second offset
        custom_clock = CustomClock(time_offset_ms=5000)
        limiter = RateLimiter(max_rps=1, clock=custom_clock)
        
        # The rate limiter will use the custom clock with offset
        # This could be useful for testing timezone differences or clock synchronization
        self.assertTrue(limiter.is_allowed())   # PASS
        self.assertFalse(limiter.is_allowed())  # FAIL (same second)
        
        # The custom clock adds 5 seconds to the current time
        # So the actual time used will be current_time + 5000ms
        current_count = limiter.get_current_count()
        self.assertEqual(current_count, 1)  # Should have 1 request in the window


if __name__ == "__main__":
    # Run the unittest tests
    unittest.main(verbosity=2)

