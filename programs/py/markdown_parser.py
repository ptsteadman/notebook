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
    TOKENS = {"*": "i", "**": "b", "~~": "s"}
    res = []
    i, stack = 0, []
    while i < len(text):
        token = text[i]
        if text[i:i+2] in TOKENS: 
            token = text[i] if (stack and stack[-1] == text[i]) else text[i:i+2]

        if token in TOKENS:
            if stack and stack[-1] == token:
                stack.pop()
                res.append(f"</{TOKENS[token]}>")
            else:
                stack.append(token)
                res.append(f"<{TOKENS[token]}>")
        else:
            res.append(text[i])
        i += len(token)
    if stack:
        res.append(f"</{TOKENS[stack[-1]]}>")

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

    def test_bold(self):
        self.assertEqual(
            parseMarkdown("Hello *world*, how **are you**?"), 
            "Hello <i>world</i>, how <b>are you</b>?",
             "italic and bold "
        )

        self.assertEqual(
            parseMarkdown("Hello *world, how **are you**?*"), 
            "Hello <i>world, how <b>are you</b>?</i>",
             "nested"
        )

    def test_strikethrough(self):
        self.assertEqual(
            parseMarkdown("Hello ~~world~~"), 
            "Hello <s>world</s>",
            "basic strikethrough"
        )
        
        self.assertEqual(
            parseMarkdown("~~strike~~ and *italic* and **bold**"), 
            "<s>strike</s> and <i>italic</i> and <b>bold</b>",
            "mixed formatting"
        )

    def test_empty_and_edge_cases(self):
        # Empty string
        self.assertEqual(parseMarkdown(""), "", "empty string")
        
        # No formatting
        self.assertEqual(parseMarkdown("plain text"), "plain text", "no formatting")
        
        # Single asterisk
        self.assertEqual(parseMarkdown("*"), "<i></i>", "single asterisk")
        
        # Double asterisk
        self.assertEqual(parseMarkdown("**"), "<b></b>", "double asterisk")
        
    def test_unmatched_tokens(self):
        # Unmatched single asterisk
        self.assertEqual(
            parseMarkdown("Hello *world"), 
            "Hello <i>world</i>",
            "unmatched single asterisk"
        )
        
        # Unmatched double asterisk
        self.assertEqual(
            parseMarkdown("Hello **world"), 
            "Hello <b>world</b>",
            "unmatched double asterisk"
        )
        
        # Unmatched strikethrough
        self.assertEqual(
            parseMarkdown("Hello ~~world"), 
            "Hello <s>world</s>",
            "unmatched strikethrough"
        )

    def test_consecutive_tokens(self):
        # Consecutive asterisks
        self.assertEqual(
            parseMarkdown("***bold***"), 
            "<b><i>bold</i></b>",
            "consecutive asterisks - bold then italic"
        )
        
        # Multiple consecutive
        self.assertEqual(
            parseMarkdown("****"), 
            "<b><i></i></b>",
            "four consecutive asterisks"
        )

    def test_nested_formatting(self):
        # Nested bold in italic
        self.assertEqual(
            parseMarkdown("*italic with **bold** inside*"), 
            "<i>italic with <b>bold</b> inside</i>",
            "bold nested in italic"
        )
        
        # Nested italic in bold
        self.assertEqual(
            parseMarkdown("**bold with *italic* inside**"), 
            "<b>bold with <i>italic</i> inside</b>",
            "italic nested in bold"
        )
        
        # Complex nesting
        self.assertEqual(
            parseMarkdown("*italic **bold ~~strike~~** text*"), 
            "<i>italic <b>bold <s>strike</s></b> text</i>",
            "complex nesting"
        )

    def test_mixed_formatting(self):
        # All three formats
        self.assertEqual(
            parseMarkdown("*italic* **bold** ~~strike~~"), 
            "<i>italic</i> <b>bold</b> <s>strike</s>",
            "all three formats"
        )
        
        # Mixed with regular text
        self.assertEqual(
            parseMarkdown("Start *italic* middle **bold** end ~~strike~~"), 
            "Start <i>italic</i> middle <b>bold</b> end <s>strike</s>",
            "mixed with regular text"
        )

    def test_special_characters(self):
        # Asterisks in content
        self.assertEqual(
            parseMarkdown("Text with *asterisk* inside"), 
            "Text with <i>asterisk</i> inside",
            "asterisk in content"
        )
        
        # Multiple asterisks in content
        self.assertEqual(
            parseMarkdown("Text with **multiple** asterisks"), 
            "Text with <b>multiple</b> asterisks",
            "multiple asterisks in content"
        )

    def test_edge_case_combinations(self):
        # Empty formatting
        self.assertEqual(
            parseMarkdown("**"), 
            "<b></b>",
            "empty bold"
        )
        
        # Mixed empty and filled
        self.assertEqual(
            parseMarkdown("** **"), 
            "<b> </b>",
            "bold with space"
        )
        

    def test_complex_scenarios(self):
        # Real-world example
        self.assertEqual(
            parseMarkdown("This is *italic* and this is **bold** and ~~strikethrough~~"), 
            "This is <i>italic</i> and this is <b>bold</b> and <s>strikethrough</s>",
            "real-world example"
        )
        
        # With punctuation
        self.assertEqual(
            parseMarkdown("Hello *world*! How **are** you?"), 
            "Hello <i>world</i>! How <b>are</b> you?",
            "with punctuation"
        )


if __name__ == '__main__':
    unittest.main()
