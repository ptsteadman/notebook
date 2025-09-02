"""
Given A and B two interval lists, A has no overlap inside A and B has no overlap inside B. Write the function to merge two interval lists, output the result with no overlap. Ask for a very efficient solution

A naive method can combine the two list, and sort and apply merge interval in the leetcode, but is not efficient enough.

For example,
A: [1,5], [10,14], [16,18]
B: [2,6], [8,10], [11,20]

output [1,6], [8, 20]
"""

from typing import List

import unittest

def interval_list_union(list_one: List[List], list_two: List[List]) -> List[List]:
    p1, p2 = 0, 0
    res = []
    curr = None
    while p1 < len(list_one) or p2 < len(list_two):
        if p1 == len(list_one):
            curr = list_two[p2]
            p2 += 1
        elif p2 == len(list_two):
            curr = list_one[p1]
            p1 += 1
        elif list_one[p1][0] < list_two[p2][0]:
            curr = list_one[p1]
            p1 += 1
        else:
            curr = list_two[p2]
            p2 += 1

        if not res or res[-1][1] < curr[0]:
            res.append(curr)
        else:
            res[-1][1] = max(res[-1][1], curr[1])
    return res


class Tester(unittest.TestCase):
    def testAll(self):
        self.assertEqual(
            interval_list_union(
                [[1,5], [10,14], [16,18]],
                [[2,6], [8,10], [11,20]],
            )
        , 
            [[1,6], [8, 20]]
        )

if __name__ == "__main__":
    unittest.main()
