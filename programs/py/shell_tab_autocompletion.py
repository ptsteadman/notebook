"""
Shell tab autocompletion

The entire problem is set in the context of the Linux shell's tab auto-completion feature.

First Question: Given a series of files ["file1", "file2", "file_new"] and the input "f", the task is to return the auto-completion result ("file"), which is the longest common prefix of all files matching the current input.


-   b - a -
        - g - END
        - d - END

    f - i - l - e - 
                -  2 - END
                -  1 - END
                -  _ - n - e - w - END

Second Question: The files may be located in subfolders ["folder/file1", "folder/file2", "folder/file/new"]. The input does not include "/". The expected output is the auto-completion result ("folder/file"), with the requirement that if all files matching the current input are in the same folder, the shell should automatically enter that folder.

Third Question: The input may include "/".
"""

import unittest
import os

class AutoCompleter:
    def __init__(self, files=None):
        if files is None:
            files = []
        self.files = files

    def get_matching_files(self, s):
        for f in self.files:
            if f.startswith(s):
                yield f

    def autocomplete_simple(self, s: str):
        res = []
        for cs in zip(*self.get_matching_files(s)):
            if not all(c == cs[0] for c in cs):
                break
            res.append(cs[0])
        return "".join(res)



class Tester(unittest.TestCase):

    def test_init(self):
        ac = AutoCompleter(["file1", "file2", "file_new"])
        self.assertEqual(ac.autocomplete("f"), "file")
        self.assertEqual(ac.autocomplete("s"), "")
        self.assertEqual(ac.autocomplete("file_"), "file_new")

        ac = AutoCompleter(["bad", "bar", "dog", "dag"])
        self.assertEqual(ac.autocomplete("b"), "ba")
        self.assertEqual(ac.autocomplete("d"), "d")

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)

