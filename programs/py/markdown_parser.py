"""
Part 1: Basic Italic Parsing Implement a function that parses markdown text, initially supporting only italics (*).

function parseMarkdown(text: string): string;

// Examples:
parseMarkdown("Hello *world*")
// Returns: "Hello <i>world</i>"

parseMarkdown("*Hello* there *world*")
// Returns: "<i>Hello</i> there <i>world</i>"
Part 2: Extended Formatting Add support for:
- Bold (**)
- Strikethrough (~~)

Followups:
- Add validation to check if the markdown formatting is correct.
- Even when the input format is incorrect, try to produce reasonable HTML output.
"""

import unittest

def parseMarkdown(text: str) -> str:
    res = []
    last_end, last_token = 0, None
    for i, c in enumerate(text):
        if c == "*":
            if last_token is None:
                last_token = "*"
                res.extend([text[last_end:i], "<i>"])
                last_end = i + 1
            else:
                res.extend([text[last_end:i], "</i>"])
                last_token = None
                last_end = i + 1 
    res.append(text[last_end:])
    if last_token is not None:
        res.append("</i>")

    return "".join(res)

class MarkdownParserTester(unittest.TestCase):
    def test_italic(self):
        self.assertEqual(parseMarkdown("Hello *world*"), "Hello <i>world</i>", "Basic example")
        self.assertEqual(
            parseMarkdown("Hello *world*, how *are you*?"), 
            "Hello <i>world</i>, how <i>are you</i>?",
             "two italics "
        )
        self.assertEqual(
            parseMarkdown("Hello *world*, how *are you?"), 
            "Hello <i>world</i>, how <i>are you?</i>",
             "invalid"
        )


if __name__ == '__main__':
    unittest.main()
