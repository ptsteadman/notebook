"""
Implement a template parser that replaces variables in a template string using values from a provided map.

function parse(template: string, variables: Record<string, string>): string;

// Example:
parse("I like {dog}", { dog: "poodle" })
// Returns: "I like poodle"

parse("Hello {name}, welcome to {platform}", {
  name: "Alex",
  platform: "Figma"
})
// Returns: "Hello Alex, welcome to Figma"
"""

import unittest
from typing import Dict
from string import Template

def parse(template: str, variables: Dict) -> str:
    template = template.replace("{", "${")
    return Template(template).substitute(variables)

class TestTemplate(unittest.TestCase):
    def test(self):
        self.assertEqual(
            parse("I like {dog}", { "dog": "Poodle"}),
             "I like Poodle"
        )
        self.assertEqual(
            parse("Hello {name}, welcome to {platform}", { "name": "Alex"}),
            "Hello Alex, welcome to Figma"
        )

if __name__ == "__main__":
    unittest.main()

