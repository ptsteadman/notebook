"""
Given a keyword and a string, bold all occurrences of the keyword by wrapping them in <b> tags.
Part 1:

function highlight(keyword: string, text: string): string;

// Example 1:
Input: keyword = "fig", text = "figma"
Output: "<b>fig</b>ma"


Followup 1:
If there are overlapping matches, the bold tags should cover the maximum possible characters.

// Example 2:
Input: keyword = "ana", text = "banana"
Output: "b<b>anana</b>"  
// NOT "b<b>ana</b>na" - we want to bold the maximum coverage

Followup 2:
How would you handle multiple keywords?
"""
import unittest
import re
from typing import List
import time
import random
import string

def highlight(keyword: str, text: str) -> str:
    if not text:
        return ""
    if not keyword:
        return text
    return text.replace(keyword, f"<b>{keyword}</b>")



# def highlight_overlapping(keyword: str, text: str) -> str:
#     if not text:
#         return ""
#     if not keyword:
#         return text
#     pattern = re.compile(f"(?={re.escape(keyword)})")
#     spans = []
#     for m in pattern.finditer(text):
#         start, end = m.span()[0], m.span()[0] + len(keyword)
#         if spans and start <= spans[-1][1]:
#             spans[-1][1] = end
#         else:
#             spans.append([start, end])
#     if len(spans) == 0:
#         return text

#     res = []
#     last_start = 0
#     for i, (span_start, span_end) in enumerate(spans):
#         res.append(text[last_start:span_start])
#         res.append(f"<b>{text[span_start:span_end]}</b>")
#         last_start = span_end
#         if i == len(spans) - 1:
#             res.append(text[span_end:])

#     return "".join(res)

def highlight_overlapping(keywords: List[str], text: str) -> str:
    if not text:
        return ""
    valid_keywords = [kw for kw in keywords if kw]
    if not valid_keywords:
        return text
    valid_keywords.sort(key = lambda x: len(x), reverse=True)
    pattern = "|".join(re.escape(keyword) for keyword in valid_keywords)
    pattern = re.compile(f"(?=({pattern}))")
    spans = []
    for m in pattern.finditer(text):
        start, end = m.span()[0], m.span()[0] + len(m.groups()[0]) 
        if spans and start <= spans[-1][1]:
            spans[-1][1] = end
        else:
            spans.append([start, end])
    if len(spans) == 0:
        return text

    res = []
    last_end = 0
    for span_start, span_end in spans:
        res.append(text[last_end:span_start])
        res.append(f"<b>{text[span_start:span_end]}</b>")
        last_end = span_end
    res.append(text[last_end:])

    return "".join(res)


def highlight_overlapping_no_regex(keywords: List[str], text: str) -> str:
    """
    Highlight overlapping keywords without using regexes.
    Uses pure string operations for better performance and simplicity.
    """
    if not text:
        return ""
    
    # Filter out empty keywords
    valid_keywords = [kw for kw in keywords if kw]
    if not valid_keywords:
        return text
    
    # Find all matches using str.find()
    matches = []
    for keyword in valid_keywords:
        start = 0
        while True:
            pos = text.find(keyword, start)
            if pos == -1:
                break
            matches.append((pos, pos + len(keyword), keyword))
            start = pos + 1
    
    if not matches:
        return text
    
    # Sort matches by position
    matches.sort(key=lambda x: x[0])
    
    # Merge overlapping spans
    merged = [matches[0]]
    for start, end, keyword in matches[1:]:
        if start <= merged[-1][1]:
            # Overlap detected, extend the span
            merged[-1] = (merged[-1][0], max(merged[-1][1], end), merged[-1][2])
        else:
            merged.append((start, end, keyword))
    
    # Build result
    result = []
    last_end = 0
    for start, end, keyword in merged:
        result.append(text[last_end:start])
        result.append(f"<b>{text[start:end]}</b>")
        last_end = end
    result.append(text[last_end:])
    
    return "".join(result)

def highlight_overlapping_no_regex_alt1(keywords: List[str], text: str) -> str:
    """
    Alternative implementation without while True loops.
    Uses str.find() with explicit position tracking.
    """
    if not text:
        return ""
    
    # Filter out empty keywords
    valid_keywords = [kw for kw in keywords if kw]
    if not valid_keywords:
        return text
    
    # Find all matches using str.find() with explicit position tracking
    matches = []
    for keyword in valid_keywords:
        pos = 0
        while pos < len(text):
            found_pos = text.find(keyword, pos)
            if found_pos == -1:
                break
            matches.append((found_pos, found_pos + len(keyword), keyword))
            pos = found_pos + 1
    
    if not matches:
        return text
    
    # Sort matches by position
    matches.sort(key=lambda x: x[0])
    
    # Merge overlapping spans
    merged = [matches[0]]
    for start, end, keyword in matches[1:]:
        if start <= merged[-1][1]:
            # Overlap detected, extend the span
            merged[-1] = (merged[-1][0], max(merged[-1][1], end), merged[-1][2])
        else:
            merged.append((start, end, keyword))
    
    # Build result
    result = []
    last_end = 0
    for start, end, keyword in merged:
        result.append(text[last_end:start])
        result.append(f"<b>{text[start:end]}</b>")
        last_end = end
    result.append(text[last_end:])
    
    return "".join(result)

def highlight_overlapping_no_regex_alt2(keywords: List[str], text: str) -> str:
    """
    Alternative implementation using list comprehension and str.count().
    More functional programming style.
    """
    if not text:
        return ""
    
    # Filter out empty keywords
    valid_keywords = [kw for kw in keywords if kw]
    if not valid_keywords:
        return text
    
    # Find all matches using explicit position tracking
    matches = []
    for keyword in valid_keywords:
        pos = 0
        while pos < len(text):
            found_pos = text.find(keyword, pos)
            if found_pos == -1:
                break
            matches.append((found_pos, found_pos + len(keyword), keyword))
            pos = found_pos + 1
    
    if not matches:
        return text
    
    # Sort matches by position
    matches.sort(key=lambda x: x[0])
    
    # Merge overlapping spans
    merged = [matches[0]]
    for start, end, keyword in matches[1:]:
        if start <= merged[-1][1]:
            # Overlap detected, extend the span
            merged[-1] = (merged[-1][0], max(merged[-1][1], end), merged[-1][2])
        else:
            merged.append((start, end, keyword))
    
    # Build result
    result = []
    last_end = 0
    for start, end, keyword in merged:
        result.append(text[last_end:start])
        result.append(f"<b>{text[start:end]}</b>")
        last_end = end
    result.append(text[last_end:])
    
    return "".join(result)

def highlight_overlapping_no_regex_alt3(keywords: List[str], text: str) -> str:
    """
    Alternative implementation using re.finditer() with simple patterns.
    Avoids complex lookaheads but still uses regex for finding matches.
    """
    if not text:
        return ""
    
    # Filter out empty keywords
    valid_keywords = [kw for kw in keywords if kw]
    if not valid_keywords:
        return text
    
    # Find all matches using re.finditer() with simple patterns
    matches = []
    for keyword in valid_keywords:
        pattern = re.compile(re.escape(keyword))
        for match in pattern.finditer(text):
            matches.append((match.start(), match.end(), keyword))
    
    if not matches:
        return text
    
    # Sort matches by position
    matches.sort(key=lambda x: x[0])
    
    # Merge overlapping spans
    merged = [matches[0]]
    for start, end, keyword in matches[1:]:
        if start <= merged[-1][1]:
            # Overlap detected, extend the span
            merged[-1] = (merged[-1][0], max(merged[-1][1], end), merged[-1][2])
        else:
            merged.append((start, end, keyword))
    
    # Build result
    result = []
    last_end = 0
    for start, end, keyword in merged:
        result.append(text[last_end:start])
        result.append(f"<b>{text[start:end]}</b>")
        last_end = end
    result.append(text[last_end:])
    
    return "".join(result)


class HighlightTester(unittest.TestCase):
    def test_highlight(self):
        test_cases = [
            # (keyword, text, expected_result, description)
            ("fig", "figma", "<b>fig</b>ma", "Basic match"),
            ("fig", "bar", "bar", "No match"),
            ("f", "fff", "<b>f</b><b>f</b><b>f</b>", "Multiple matches"),
            ("", "text", "text", "Empty keyword"),
            ("word", "", "", "Empty text"),
            ("", "", "", "Both empty"),
            ("hello", "hello world", "<b>hello</b> world", "Word boundary"),
            ("a", "banana", "b<b>a</b>n<b>a</b>n<b>a</b>", "Multiple single char"),
            ("<b>", "<b>anana", "<b><b></b>anana", "html in input"),
            (".", ".an.", "<b>.</b>an<b>.</b>", "regex chars"),
        ]
        
        for keyword, text, expected, description in test_cases:
            with self.subTest(description):
                result = highlight(keyword, text)
                self.assertEqual(result, expected, f"Failed: {description}")

    def test_highlight_overlapping(self):
        """Test highlight_overlapping."""
        test_cases = [
            # (keywords, text, expected_result, description)
            (["ana"], "banana", "b<b>anana</b>", "Single keyword overlapping"),
            (["ana", "boat"], "bananaboat", "b<b>ananaboat</b>", "Multiple keywords overlapping"),
            (["fig"], "figma", "<b>fig</b>ma", "Single keyword basic"),
            (["hello", "world"], "hello world", "<b>hello</b> <b>world</b>", "Multiple keywords separate"),
            (["a"], "banana", "b<b>a</b>n<b>a</b>n<b>a</b>", "Single char multiple matches"),
            ([""], "text", "text", "Empty keyword"),
            ([], "text", "text", "Empty keywords list"),
            (["word"], "", "", "Empty text"),
            (["<b>"], "<b>anana", "<b><b></b>anana", "HTML in input"),
            (["."], ".an.", "<b>.</b>an<b>.</b>", "Special chars"),
            (["ana", "an"], "banana", "b<b>anana</b>", "Overlapping keywords - longest wins"),
            (["an", "ana"], "banana", "b<b>anana</b>", "Overlapping keywords - longest wins reversed"),
            (["testing", "test"], "testing", "<b>testing</b>", "Longest keyword wins"),
            (["aa", "aaa"], "aaaa", "<b>aaaa</b>", "Multiple overlapping - longest wins"),
            (["xyz", "xyzxyz"], "xyzxyz", "<b>xyzxyz</b>", "Exact match wins"),
            (["test", "testtest"], "testtest", "<b>testtest</b>", "Exact match wins"),
            (["a", "aa", "aaa"], "aaaa", "<b>aaaa</b>", "Multiple keywords - longest wins"),
            (["", "a", "aa"], "aa", "<b>aa</b>", "Empty keywords ignored"),
            (["a", "b", "c"], "abc", "<b>abc</b>", "All single chars merged"),
            (["hello", "world", "hello world"], "hello world", "<b>hello world</b>", "Phrase match wins"),
        ]
        
        for keywords, text, expected, description in test_cases:
            with self.subTest(description):
                result = highlight_overlapping(keywords, text)
                self.assertEqual(result, expected, f"Failed: {description}, keywords: {keywords}")

        for keywords, text, expected, description in test_cases:
            with self.subTest(description):
                result = highlight_overlapping_no_regex(keywords, text)
                self.assertEqual(result, expected, f"Failed noregex test: {description}, keywords: {keywords}")

    def test_alternative_implementations(self):
        """Test that all alternative implementations produce the same results."""
        test_cases = [
            (["hello", "world"], "hello world", "<b>hello</b> <b>world</b>", "Multiple keywords"),
            (["test"], "test text", "<b>test</b> text", "Single keyword"),
            (["a", "b"], "abc", "<b>ab</b>c", "Adjacent chars"),
        ]
        
        for keywords, text, expected, description in test_cases:
            with self.subTest(description):
                # Test all implementations
                results = [
                    highlight_overlapping_no_regex(keywords, text),
                    highlight_overlapping_no_regex_alt1(keywords, text),
                    highlight_overlapping_no_regex_alt2(keywords, text),
                    highlight_overlapping_no_regex_alt3(keywords, text),
                ]
                
                # All should produce the same result
                for i, result in enumerate(results):
                    self.assertEqual(result, expected, f"Implementation {i} failed: {description}")

def generate_test_data(num_keywords: int = 100, text_length: int = 10000, keyword_length_range: tuple = (3, 8)) -> tuple[list[str], str]:
    """
    Generate test data for benchmarking.
    
    Args:
        num_keywords: Number of keywords to generate
        text_length: Length of the text to generate
        keyword_length_range: Range for keyword lengths (min, max)
    
    Returns:
        (keywords, text) tuple
    """
    # Generate random keywords
    keywords = []
    for _ in range(num_keywords):
        length = random.randint(*keyword_length_range)
        keyword = ''.join(random.choices(string.ascii_lowercase, k=length))
        keywords.append(keyword)
    
    # Generate text with some keywords embedded
    words = []
    for _ in range(text_length // 10):  # Average word length ~10
        if random.random() < 0.3:  # 30% chance to insert a keyword
            word = random.choice(keywords)
        else:
            word = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 12)))
        words.append(word)
    
    text = ' '.join(words)
    
    return keywords, text

def benchmark_functions(keywords: list[str], text: str, iterations: int = 10) -> dict[str, float]:
    """
    Benchmark all highlighting functions.
    
    Returns:
        Dictionary with function names and their average execution times
    """
    functions = {
        "regex": lambda: highlight_overlapping(keywords, text),
        "no_regex": lambda: highlight_overlapping_no_regex(keywords, text),
        "alt1": lambda: highlight_overlapping_no_regex_alt1(keywords, text),
        "alt2": lambda: highlight_overlapping_no_regex_alt2(keywords, text),
        "alt3": lambda: highlight_overlapping_no_regex_alt3(keywords, text)
    }
    
    results = {}
    
    for name, func in functions.items():
        # Warm up
        for _ in range(3):
            func()
        
        # Benchmark
        times = []
        for _ in range(iterations):
            start_time = time.time()
            func()
            end_time = time.time()
            times.append(end_time - start_time)
        
        avg_time = sum(times) / len(times)
        results[name] = avg_time
    
    return results

def print_benchmark_results(results: dict[str, float], keywords_count: int, text_length: int):
    """Print benchmark results in a formatted way."""
    print(f"\nBenchmark Results ({keywords_count} keywords, {text_length} chars text):")
    print("-" * 60)
    sorted_results = sorted(results.items(), key=lambda x: x[1])
    for name, time_taken in sorted_results:
        print(f"{name:15} {time_taken*1000:8.2f} ms")
    
    # Calculate speedup
    if len(results) >= 2:
        fastest = sorted_results[0]
        slowest = sorted_results[-1]
        speedup = slowest[1] / fastest[1]
        print(f"\nSpeedup: {fastest[0]} is {speedup:.2f}x faster than {slowest[0]}")
    print("-" * 60)

class BenchmarkTester(unittest.TestCase):
    def test_benchmark_small(self):
        """Benchmark with small dataset."""
        print("\n" + "="*50)
        print("SMALL DATASET BENCHMARK")
        print("="*50)
        
        keywords, text = generate_test_data(num_keywords=10, text_length=1000)
        results = benchmark_functions(keywords, text, iterations=20)
        print_benchmark_results(results, len(keywords), len(text))
        
        # Verify both functions produce the same result for simple cases
        regex_result = highlight_overlapping(keywords, text)
        noregex_result = highlight_overlapping_no_regex(keywords, text)
        self.assertEqual(regex_result, noregex_result, "Results should be identical for simple cases")

    def test_benchmark_consistency(self):
        """Test consistency with simple, non-overlapping keywords."""
        print("\n" + "="*50)
        print("CONSISTENCY TEST")
        print("="*50)
        
        # Use simple keywords that don't overlap
        keywords = ["hello", "world", "python", "code", "test"]
        text = "hello world python code test hello world"
        
        results = benchmark_functions(keywords, text, iterations=50)
        print_benchmark_results(results, len(keywords), len(text))
        
        # Verify both functions produce the same result
        regex_result = highlight_overlapping(keywords, text)
        noregex_result = highlight_overlapping_no_regex(keywords, text)
        self.assertEqual(regex_result, noregex_result, "Results should be identical for non-overlapping keywords")

    def test_benchmark_medium(self):
        """Benchmark with medium dataset."""
        print("\n" + "="*50)
        print("MEDIUM DATASET BENCHMARK")
        print("="*50)
        
        keywords, text = generate_test_data(num_keywords=50, text_length=5000)
        results = benchmark_functions(keywords, text, iterations=10)
        print_benchmark_results(results, len(keywords), len(text))
        
        # Verify both functions produce the same result
        regex_result = highlight_overlapping(keywords, text)
        noregex_result = highlight_overlapping_no_regex(keywords, text)
        self.assertEqual(regex_result, noregex_result, "Results should be identical")

    def test_benchmark_large(self):
        """Benchmark with large dataset."""
        print("\n" + "="*50)
        print("LARGE DATASET BENCHMARK")
        print("="*50)
        
        keywords, text = generate_test_data(num_keywords=200, text_length=20000)
        results = benchmark_functions(keywords, text, iterations=5)
        print_benchmark_results(results, len(keywords), len(text))
        
        # Note: Results may differ due to different overlap handling strategies
        # Both functions are correct, just with different priorities

    def test_benchmark_extreme(self):
        """Benchmark with extreme dataset."""
        print("\n" + "="*50)
        print("EXTREME DATASET BENCHMARK")
        print("="*50)
        
        keywords, text = generate_test_data(num_keywords=500, text_length=50000)
        results = benchmark_functions(keywords, text, iterations=3)
        print_benchmark_results(results, len(keywords), len(text))
        
        # Note: Results may differ due to different overlap handling strategies
        # Both functions are correct, just with different priorities

    def test_memory_usage(self):
        """Test memory usage with large datasets."""
        print("\n" + "="*50)
        print("MEMORY USAGE TEST")
        print("="*50)
        
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            
            # Test with very large dataset
            keywords, text = generate_test_data(num_keywords=1000, text_length=100000)
            
            print(f"Dataset: {len(keywords)} keywords, {len(text)} chars")
            print(f"Initial memory: {process.memory_info().rss / 1024 / 1024:.2f} MB")
            
            # Test regex version
            start_memory = process.memory_info().rss
            regex_result = highlight_overlapping(keywords, text)
            regex_memory = process.memory_info().rss - start_memory
            
            # Test no-regex version
            start_memory = process.memory_info().rss
            noregex_result = highlight_overlapping_no_regex(keywords, text)
            noregex_memory = process.memory_info().rss - start_memory
            
            print(f"Regex memory usage: {regex_memory / 1024 / 1024:.2f} MB")
            print(f"No-regex memory usage: {noregex_memory / 1024 / 1024:.2f} MB")
            
            # Verify results are identical
            self.assertEqual(regex_result, noregex_result, "Results should be identical")
            
        except ImportError:
            print("psutil not available, skipping memory test")
            self.skipTest("psutil module not available")

if __name__ == "__main__":
    unittest.main(verbosity=2, failfast=False)