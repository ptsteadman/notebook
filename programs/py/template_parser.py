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
import re

def parse(template: str, variables: Dict) -> str:
    """
    Parse a template string with support for escaping braces.
    
    {{ and }} are treated as literal braces
    {var} is treated as a variable placeholder
    """
    if not template:
        return template
    
    # Step 1: Replace escaped braces with temporary placeholders
    # {{ -> TEMP_OPEN_BRACE, }} -> TEMP_CLOSE_BRACE
    temp_template = template.replace("{{", "TEMP_OPEN_BRACE")
    temp_template = temp_template.replace("}}", "TEMP_CLOSE_BRACE")
    
    # Step 2: Convert single braces to Template format
    # {var} -> ${var}
    fixed_template = re.sub(r'\{([^}]+)\}', r'$\1', temp_template)
    
    # Step 3: Substitute variables
    result = Template(fixed_template).substitute(variables)
    
    # Step 4: Convert temporary placeholders back to braces
    result = result.replace("TEMP_OPEN_BRACE", "{")
    result = result.replace("TEMP_CLOSE_BRACE", "}")
    
    return result

class TestTemplate(unittest.TestCase):
    def test_basic_substitution(self):
        self.assertEqual(
            parse("I like {dog}", {"dog": "Poodle"}),
            "I like Poodle"
        )
    
    def test_multiple_variables(self):
        self.assertEqual(
            parse("Hello {name}, welcome to {platform}", {"name": "Alex", "platform": "figma"}),
            "Hello Alex, welcome to figma"
        )
    
    def test_missing_variable_raises_keyerror(self):
        with self.assertRaises(KeyError):
            parse("Hello {name}, welcome to {platform}", {"name": "Alex"})
    
    def test_escaped_braces(self):
        # Test that {{ and }} are treated as literal braces
        self.assertEqual(
            parse("function {functionName} {{}}", {"functionName": "hello"}),
            "function hello {}"
        )
    
    def test_mixed_escaped_and_variables(self):
        self.assertEqual(
            parse("Hello {name}, your code: {{x + y}}", {"name": "Alex"}),
            "Hello Alex, your code: {x + y}"
        )
    
    def test_only_escaped_braces(self):
        self.assertEqual(
            parse("This is literal: {{}}", {}),
            "This is literal: {}"
        )
    
    def test_malformed_template(self):
        # Test that malformed templates (unmatched braces) are handled gracefully
        # The current implementation will leave unmatched braces as-is
        result = parse("Hello {name}, welcome to {platform", {"name": "Alex"})
        self.assertEqual(result, "Hello Alex, welcome to {platform")

if __name__ == "__main__":
    unittest.main()

