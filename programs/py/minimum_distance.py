"""
Find the minimum distance between the indices (positions) of two given words within a list of words.

Example:

Input: S = { “the”, “quick”, “brown”, “fox”, “quick”}, word1 = “the”, word2 = “fox”
Output: 3
Explanation: Minimum distance between the words “the” and “fox” is 3

Input: S = {“geeks”, “for”, “geeks”, “contribute”,  “practice”}, word1 = “geeks”, word2 = “practice”
Output: 2
Explanation: Minimum distance between the words “geeks” and “practice” is 2

"""
from typing import List
import unittest

def minimum_distance(words: List[str], word1: str, word2: str) -> int:
    res = float('inf')
    i_word1, i_word2 = None, None
    for i, w in enumerate(words):
        if w == word1:
            i_word1 = i
        if w == word2:
            i_word2 = i
        if i_word1 is not None and i_word2 is not None and i_word1 != i_word2:
            res = min(res, abs(i_word1 - i_word2))
    return res if res != float('inf') else -1

class MinimumDistanceTester(unittest.TestCase):
    def test_basic(self):
        s1 = ["the", "quick", "brown", "fox", "quick"] 
        self.assertEqual(minimum_distance(s1, "the", "fox"), 3)
        s2 = ["geeks", "for", "geeks", "contribute", "practice"] 
        self.assertEqual(minimum_distance(s2, "geeks", "practice"), 2)
        self.assertEqual(minimum_distance(s2, "geeks", "contribute"), 1)
        self.assertEqual(minimum_distance(s2, "foo", "bar"), -1)

if __name__ == "__main__":
    unittest.main()