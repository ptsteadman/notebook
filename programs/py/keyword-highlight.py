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
    if not keywords or (len(keywords) == 1 and not keywords[0]):
        return text
    pattern = "|".join(re.escape(keyword) for keyword in keywords)
    pattern = re.compile(f"(?=({pattern}))")
    spans = []
    for m in pattern.finditer(text):
        print(m.groups())
        start, end = m.span()[0], m.span()[0] + len(m.groups()[0]) 
        if spans and start <= spans[-1][1]:
            spans[-1][1] = end
        else:
            spans.append([start, end])
    if len(spans) == 0:
        return text

    res = []
    last_start = 0
    for i, (span_start, span_end) in enumerate(spans):
        res.append(text[last_start:span_start])
        res.append(f"<b>{text[span_start:span_end]}</b>")
        last_start = span_end
        if i == len(spans) - 1:
            res.append(text[span_end:])

    return "".join(res)

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
        test_cases = [
            # (keyword, text, expected_result, description)
            ("ana", "banana", "b<b>anana</b>", "Overlapping matches"),
            ("fig", "figma", "<b>fig</b>ma", "Basic match"),
            ("fig", "bar", "bar", "No match"),
            ("f", "fff", "<b>fff</b>", "Overlapping matches"),
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
                result = highlight_overlapping([keyword], text)
                self.assertEqual(result, expected, f"Failed: {description}")


    def test_highlight_overlapping_muptile(self):
        test_cases = [
            # (keyword, text, expected_result, description)
            (["ana", "boat"], "bananaboat", "b<b>ananaboat</b>", "Overlapping matches"),
            (["ana"], "bananaboat", "b<b>anana</b>boat", "Overlapping matches"),
        ]
        
        for keywords, text, expected, description in test_cases:
            with self.subTest(description):
                result = highlight_overlapping(keywords, text)
                self.assertEqual(result, expected, f"Failed: {description}")

if __name__ == "__main__":
    unittest.main(verbosity=2, failfast=True)