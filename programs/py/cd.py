import unittest

def cd(current: str, path: str) -> str:
    joined_path = path if path.startswith('/') else f"{current.rstrip('/')}/{path.lstrip('/')}"
    stack = []
    for part in joined_path.split('/'):
        if part == ".." and stack:
            breakpoint()
            stack.pop()
        elif part and part != ".":
            stack.append(part)

    return "/" + "/".join(stack)


class Tester(unittest.TestCase):
    def test_subdir(self):
        self.assertEqual(cd("/b", "a"), "/b/a")
        self.assertEqual(cd("/b", "c"), "/b/c")

    def test_abs(self):
        self.assertEqual(cd("/b", "/e"), "/e")

    def test_relative(self):
        self.assertEqual(cd("/x/y", "../p/q"), "/x/p/q")
        self.assertEqual(cd("/x/y", "p/./q"), "/x/y/p/q")

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
