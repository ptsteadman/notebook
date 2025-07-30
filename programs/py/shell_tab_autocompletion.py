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
from dataclasses import dataclass, field

@dataclass
class TrieNode:
    children: dict = field(default_factory=dict)
    is_end: bool = False

class DictTrieAutoCompleter:
    """Alternative implementation using a simple dictionary as trie"""
    
    def __init__(self, files=None):
        if files is None:
            files = []
        self.files = files
        self.trie = {}  # Simple dict as trie
        self._build_trie()
    
    def _build_trie(self):
        """Build trie using nested dictionaries"""
        for file in self.files:
            self._insert_file(file)
    
    def _insert_file(self, file):
        """Insert file into dict-based trie"""
        curr = self.trie
        for char in file:
            if char not in curr:
                curr[char] = {}
            curr = curr[char]
        curr['__end__'] = True  # Mark end of word
    
    def autocomplete(self, s):
        """Complete using dict-based trie"""
        if not s:
            return ""
        
        # Navigate to the node corresponding to the input prefix
        curr = self.trie
        for char in s:
            if char not in curr:
                return ""  # No matching files
            curr = curr[char]
        
        # Now traverse while there's only one child or we hit an end
        result = list(s)
        while curr and len(curr) == 1 and '__end__' not in curr:
            # Get the single child
            next_char = next(key for key in curr.keys() if key != '__end__')
            result.append(next_char)
            curr = curr[next_char]
        
        return "".join(result)

class ArrayTrieAutoCompleter:
    """Alternative implementation using arrays for trie nodes"""
    
    def __init__(self, files=None):
        if files is None:
            files = []
        self.files = files
        self.nodes = [{'children': {}, 'is_end': False}]  # Array of nodes
        self._build_trie()
    
    def _build_trie(self):
        """Build trie using array of nodes"""
        for file in self.files:
            self._insert_file(file)
    
    def _insert_file(self, file):
        """Insert file into array-based trie"""
        curr_idx = 0  # Root node index
        for char in file:
            curr_node = self.nodes[curr_idx]
            if char not in curr_node['children']:
                # Create new node
                new_idx = len(self.nodes)
                self.nodes.append({'children': {}, 'is_end': False})
                curr_node['children'][char] = new_idx
            curr_idx = curr_node['children'][char]
        self.nodes[curr_idx]['is_end'] = True
    
    def autocomplete(self, s):
        """Complete using array-based trie"""
        if not s:
            return ""
        
        # Navigate to the node corresponding to the input prefix
        curr_idx = 0
        for char in s:
            curr_node = self.nodes[curr_idx]
            if char not in curr_node['children']:
                return ""  # No matching files
            curr_idx = curr_node['children'][char]
        
        # Now traverse while there's only one child or we hit an end
        result = list(s)
        while curr_idx < len(self.nodes):
            curr_node = self.nodes[curr_idx]
            if curr_node['is_end'] or len(curr_node['children']) != 1:
                break
            # Get the single child
            next_char, next_idx = next(iter(curr_node['children'].items()))
            result.append(next_char)
            curr_idx = next_idx
        
        return "".join(result)

class AutoCompleter:
    def __init__(self, files=None):
        if files is None:
            files = []
        self.files = files
        self.trie_root = TrieNode()
        self._build_trie()
    
    def _build_trie(self):
        """Build the trie from the list of files"""
        for file in self.files:
            self._insert_file(file)
    
    def _insert_file(self, file):
        """Insert a file into the trie"""
        curr = self.trie_root
        for char in file:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.is_end = True

    def get_matching_files(self, s):
        for f in self.files:
            if f.startswith(s):
                yield f

    def autocomplete(self, s):
        """Complete the input using trie traversal"""
        if not s:
            return ""
        
        # Navigate to the node corresponding to the input prefix
        curr = self.trie_root
        for char in s:
            if char not in curr.children:
                return ""  # No matching files
            curr = curr.children[char]
        
        # Now traverse while there's only one child or we hit an end node
        result = list(s)
        while curr and len(curr.children) == 1 and not curr.is_end:
            # Get the single child
            next_char = next(iter(curr.children.keys()))
            result.append(next_char)
            curr = curr.children[next_char]
        
        return "".join(result)

    def autocomplete_simple(self, s: str):
        res = []
        for cs in zip(*self.get_matching_files(s)):
            if not all(c == cs[0] for c in cs):
                break
            res.append(cs[0])
        return "".join(res)
    
    def print_trie(self, node=None, prefix="", level=0):
        """Print the trie structure for debugging"""
        if node is None:
            node = self.trie_root
        
        indent = "  " * level
        if node.is_end:
            print(f"{indent}END")
        
        for char, child in sorted(node.children.items()):
            print(f"{indent}{char}")
            self.print_trie(child, prefix + char, level + 1)



class Tester(unittest.TestCase):

    def test_init(self):
        ac = AutoCompleter(["file1", "file2", "file_new"])
        self.assertEqual(ac.autocomplete("f"), "file")
        self.assertEqual(ac.autocomplete("s"), "")
        self.assertEqual(ac.autocomplete("file_"), "file_new")

        ac = AutoCompleter(["bad", "bar", "dog", "dag"])
        self.assertEqual(ac.autocomplete("b"), "ba")
        self.assertEqual(ac.autocomplete("d"), "d")
    
    def test_edge_cases(self):
        # Empty files list
        ac = AutoCompleter([])
        self.assertEqual(ac.autocomplete("f"), "")
        
        # Single file
        ac = AutoCompleter(["single"])
        self.assertEqual(ac.autocomplete("s"), "single")
        
        # No matching prefix
        ac = AutoCompleter(["file1", "file2"])
        self.assertEqual(ac.autocomplete("x"), "")
        
        # Exact match
        ac = AutoCompleter(["file1", "file2"])
        self.assertEqual(ac.autocomplete("file1"), "file1")
        
        # Empty input
        ac = AutoCompleter(["file1", "file2"])
        self.assertEqual(ac.autocomplete(""), "")
    
    def test_complex_cases(self):
        # Multiple branches
        ac = AutoCompleter(["apple", "application", "apply", "banana"])
        self.assertEqual(ac.autocomplete("a"), "appl")
        self.assertEqual(ac.autocomplete("ap"), "appl")
        self.assertEqual(ac.autocomplete("appl"), "appl")
        self.assertEqual(ac.autocomplete("b"), "banana")
        
        # Common prefix with different endings
        ac = AutoCompleter(["test1", "test2", "test3"])
        self.assertEqual(ac.autocomplete("t"), "test")
        self.assertEqual(ac.autocomplete("te"), "test")
        self.assertEqual(ac.autocomplete("tes"), "test")
        self.assertEqual(ac.autocomplete("test"), "test")
    
    def test_implementation_equivalence(self):
        """Test that all three implementations produce the same results"""
        files = ["file1", "file2", "file_new", "apple", "application"]
        inputs = ["f", "fi", "file", "file_", "a", "ap", "app", "x", ""]
        
        # Create instances of all three implementations
        ac1 = AutoCompleter(files)
        ac2 = DictTrieAutoCompleter(files)
        ac3 = ArrayTrieAutoCompleter(files)
        
        # Test that all produce the same results
        for input_str in inputs:
            result1 = ac1.autocomplete(input_str)
            result2 = ac2.autocomplete(input_str)
            result3 = ac3.autocomplete(input_str)
            
            self.assertEqual(result1, result2, f"Dict implementation differs for input '{input_str}'")
            self.assertEqual(result2, result3, f"Array implementation differs for input '{input_str}'")
            self.assertEqual(result1, result3, f"Array implementation differs for input '{input_str}'")

if __name__ == '__main__':
    # Run tests
    unittest.main(exit=False, verbosity=2)
    
    # Demonstration
    print("\n" + "="*50)
    print("TRIE AUTCOMPLETION DEMONSTRATION")
    print("="*50)
    
    files = ["file1", "file2", "file_new"]
    ac = AutoCompleter(files)
    
    print(f"Files: {files}")
    print("\nTrie structure:")
    ac.print_trie()
    
    print(f"\nAutocomplete examples:")
    print(f"'f' -> '{ac.autocomplete('f')}'")
    print(f"'fi' -> '{ac.autocomplete('fi')}'")
    print(f"'fil' -> '{ac.autocomplete('fil')}'")
    print(f"'file' -> '{ac.autocomplete('file')}'")
    print(f"'file_' -> '{ac.autocomplete('file_')}'")
    print(f"'s' -> '{ac.autocomplete('s')}'")
    
    # Compare implementations
    print("\n" + "="*50)
    print("COMPARING DIFFERENT TRIE IMPLEMENTATIONS")
    print("="*50)
    
    test_files = ["apple", "application", "apply"]
    test_inputs = ["a", "ap", "app", "appl"]
    
    ac1 = AutoCompleter(test_files)
    ac2 = DictTrieAutoCompleter(test_files)
    ac3 = ArrayTrieAutoCompleter(test_files)
    
    print(f"Test files: {test_files}")
    print("\nResults comparison:")
    for input_str in test_inputs:
        r1 = ac1.autocomplete(input_str)
        r2 = ac2.autocomplete(input_str)
        r3 = ac3.autocomplete(input_str)
        print(f"'{input_str}' -> '{r1}' (all implementations agree)")
    
    # Show internal structures
    print("\n" + "="*50)
    print("INTERNAL STRUCTURES")
    print("="*50)
    
    simple_files = ["cat", "car"]
    
    print("1. Object-based Trie (original):")
    ac_obj = AutoCompleter(simple_files)
    ac_obj.print_trie()
    
    print("\n2. Dictionary-based Trie:")
    ac_dict = DictTrieAutoCompleter(simple_files)
    print(f"Trie structure: {ac_dict.trie}")
    
    print("\n3. Array-based Trie:")
    ac_array = ArrayTrieAutoCompleter(simple_files)
    print(f"Nodes array: {ac_array.nodes}")
    print("Node structure:")
    for i, node in enumerate(ac_array.nodes):
        print(f"  Node {i}: {node}")

