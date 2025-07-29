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

def highlight(keyword: str, text: str) -> str:
    if not text:
        return ""
    if not keyword:
        return text
    pattern = re.compile(re.escape(keyword))
    return pattern.sub(f"<b>{keyword}</b>", text)



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

if __name__ == "__main__":
    unittest.main(verbosity=2, failfast=False)