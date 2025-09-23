#!/usr/bin/env python3
import unittest
from query_logs.query_logs import LogQuerier
from datetime import datetime


class Tester(unittest.TestCase):
    def setUp(self):
        pass

    def test_parse_logs(self):
        q = LogQuerier("logs/test_00000.log")
        # for l in q.query(level="ERROR"):
        #     print(l)
        for l in q.query(start=datetime.fromisoformat("2025-02-28T23:55:33.888000Z")):
            print(l)



if __name__ == '__main__':
    unittest.main()
