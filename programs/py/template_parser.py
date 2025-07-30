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

def parse_old(template: str, variables: Dict) -> str:
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

def parse(template: str, variables: Dict[str, str]) -> str:
    """
    Parse a template string with support for escaping braces.
    
    {{ and }} are treated as literal braces
    {var} is treated as a variable placeholder
    Missing variables are left as {var_name}
    """
    if not template:
        return template
    
    res = []
    i = 0
    template = template.replace("{{", "TEMP_OPEN_BRACE")
    template = template.replace("}}", "TEMP_CLOSE_BRACE")
    
    while i < len(template):
        if (start := template.find("{", i)) == -1:
            res.append(template[i:])
            break
        else:
            res.append(template[i:start])
            end = template.find("}", start)
            
            if end == -1:
                # Unmatched opening brace - leave it as-is
                res.append(template[start:])
                break
            
            var_name = template[start+1:end]
            # Use .get() to handle missing variables gracefully
            res.append(variables.get(var_name, f"{{{var_name}}}"))
            i = end + 1
    
    result = "".join(res)
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
    
    def test_missing_variable_handled_gracefully(self):
        # Should leave missing variables as {var_name} instead of raising KeyError
        result = parse("Hello {name}, welcome to {platform}", {"name": "Alex"})
        self.assertEqual(result, "Hello Alex, welcome to {platform}")
    
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
    
    def test_unmatched_opening_brace(self):
        # Should handle unmatched opening brace gracefully
        result = parse("Hello {name}, welcome to {platform", {"name": "Alex"})
        self.assertEqual(result, "Hello Alex, welcome to {platform")
    
    def test_unmatched_closing_brace(self):
        # Should handle unmatched closing brace gracefully
        result = parse("Hello {name}, welcome to }platform}", {"name": "Alex"})
        self.assertEqual(result, "Hello Alex, welcome to }platform}")
    
    def test_empty_template(self):
        self.assertEqual(parse("", {"name": "Alex"}), "")
    
    def test_no_variables(self):
        self.assertEqual(parse("Hello world", {}), "Hello world")
    
    def test_empty_variables_dict(self):
        result = parse("Hello {name}", {})
        self.assertEqual(result, "Hello {name}")
    
    def test_nested_braces_in_variables(self):
        # Test that braces in variable values don't interfere
        result = parse("Hello {name}", {"name": "Alex {test}"})
        self.assertEqual(result, "Hello Alex {test}")
    
    def test_consecutive_braces(self):
        # Test handling of consecutive braces
        result = parse("Hello {name} {{}}", {"name": "Alex"})
        self.assertEqual(result, "Hello Alex {}")
    
    def test_special_characters_in_variable_names(self):
        # Test variable names with special characters
        result = parse("Hello {user_name}", {"user_name": "Alex"})
        self.assertEqual(result, "Hello Alex")

if __name__ == "__main__":
    unittest.main()

