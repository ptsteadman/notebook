import unittest

def employee_stats(orgChart: dict, employeeID: str) -> dict:

    return {}

class OrgChartTester(unittest.TestCase):
    self.org_chart = {
            "a": {
                "a1": {   
                       "a11": None,   
                       "a12": None,   
                       "a16": {
                           "a13": None,  
                           "a14": None,
                           }
                       },
                "a2": None
                },
            "b": None
            }

    def test_org_chart(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
