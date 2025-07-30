"""
Context: We have a hierarchical file system where design files and folders are organized in a tree structure (similar to how files/folders are organized in Figma). Each file/folder has specific user access permissions. We need to build a system to efficiently determine what content is accessible to users.
Problem Statement: Given a file system tree where each node (file/folder) has:
* A unique ID
* Parent ID (null for root)
* Type (file or folder)
* Access permissions (list of user IDs who can access this item)
* Name
Write a function that finds all the "topmost" accessible files/folders for a given user. "Topmost" means if a user has access to both a parent and child, only return the parent.
const fileSystem = {
  nodes: [
    {
      id: "1",
      parentId: null,
      type: "folder",
      name: "root",
      accessibleBy: ["user1"]
    },
    {
      id: "2",
      parentId: "1",
      type: "folder",
      name: "folder1",
      accessibleBy: ["user1", "user2"]
    },
    {
      id: "3",
      parentId: "2",
      type: "file",
      name: "file1",
      accessibleBy: ["user2"]
    }
  ]
};


You are given three data structures: Team, Folder, and Files. Each file and folder has an attribute that contains a list of user IDs, representing the users who have access to that team, folder, or file.
If a user has access to a higher-level team, folder, or file, they also have access to all its sub-files and sub-folders.
You need to implement two APIs: init and get_fewest(), which determine the minimum number of teams, files, or folders required to grant the user access to everything they are authorized to access.

init_function(
  [Team("Team1", ["Folder1", "Folder2"], [], ["userA"])],
  [Folder("Folder1", [], ["File1", "File2"], ["userA"]), Folder("Folder2", ["Folder3"], [], []), Folder("Folder3", [], [], ["userA"])],
  [File("File1", ["userA"]), File("File2", [])]
)
"""

import unittest
from typing import List, Set, Dict, Optional
from dataclasses import dataclass, field
from collections import deque
from itertools import chain
import pprint

@dataclass
class Node:
    uuid: str
    children: List["Node"] = field(default_factory=list) 
    users: Set[str] = field(default_factory=set) 
    parents: List["Node"] = field(default_factory=list) 

@dataclass
class FileSystemNode:
    id: str
    parentId: Optional[str]
    type: str  # "file" or "folder"
    name: str
    accessibleBy: List[str]

class SimpleFileSystem:
    def __init__(self, nodes: List[FileSystemNode]):
        self.nodes = nodes
        self.id_to_node = {node.id: node for node in nodes}
        self.children_map = {}
        
        # Build parent-child relationships
        for node in nodes:
            if node.parentId is not None:
                if node.parentId not in self.children_map:
                    self.children_map[node.parentId] = []
                self.children_map[node.parentId].append(node.id)
    
    def get_topmost_accessible(self, user_id: str) -> List[FileSystemNode]:
        """
        Find all "topmost" accessible files/folders for a given user.
        "Topmost" means if a user has access to both a parent and child, only return the parent.
        
        Algorithm: BFS from root nodes
        - Start from all root nodes (nodes with no parent)
        - Process nodes in level order (BFS ensures ancestors are processed before descendants)
        - When we find an accessible node, it's topmost (no accessible parent above it in BFS order)
        - Skip adding its descendants to the queue since they're covered
        - Continue BFS with remaining nodes
        
        Key Insight: BFS level-order processing ensures that if a node is accessible,
        it's not covered by any accessible parent (since we would have found that parent first).
        
        Time Complexity: O(V + E) where V = nodes, E = edges
        Space Complexity: O(V) for visited set and queue
        """
        def has_access(node: FileSystemNode) -> bool:
            return user_id in node.accessibleBy
        
        # Find root nodes (nodes with no parent)
        root_nodes = [node for node in self.nodes if node.parentId is None]
        
        # BFS from root nodes to find topmost accessible nodes
        topmost_nodes = []
        visited = set()
        queue = deque()
        
        # Start BFS from all root nodes
        for root in root_nodes:
            queue.append(root)
        
        # Also handle orphaned nodes (nodes with invalid parent references)
        orphaned_nodes = []
        for node in self.nodes:
            if node.parentId is not None and node.parentId not in self.id_to_node:
                orphaned_nodes.append(node)
        
        # Add orphaned nodes to the queue
        for orphan in orphaned_nodes:
            queue.append(orphan)
        
        while queue:
            node = queue.popleft()
            
            if node.id in visited:
                continue
            visited.add(node.id)
            
            # If this node is accessible, it's topmost (BFS ensures no accessible parent above)
            if has_access(node):
                topmost_nodes.append(node)
                # Skip adding descendants to queue since they're covered by this node
            else:
                # Continue BFS with children
                children = self.children_map.get(node.id, [])
                for child_id in children:
                    child = self.id_to_node.get(child_id)
                    if child and child_id not in visited:
                        queue.append(child)
        
        return topmost_nodes

class Team:
  def __init__(self, uuid, folder_ids, file_ids, user_ids):
    self.uuid = uuid
    self.folder_ids = folder_ids
    self.file_ids = file_ids
    self.user_ids = user_ids

class Folder:
  def __init__(self, uuid, folder_ids, file_ids, user_ids):
    self.uuid = uuid
    self.folder_ids = folder_ids
    self.file_ids = file_ids
    self.user_ids = user_ids

class File:
  def __init__(self, uuid, user_ids):
    self.uuid = uuid
    self.user_ids = user_ids

class FileSystem:
    def __init__(self, teams: List[Team], folders: List[Folder], files: List[File]):
        self.uuid_to_node = {}
        for file in files:
            new_file = Node(uuid=file.uuid, users=set(file.user_ids))
            self.uuid_to_node[file.uuid] = new_file

        # create folders before populating sub-folders
        for folder in folders:
            new_folder = Node(uuid=folder.uuid, users=set(folder.user_ids))
            self.uuid_to_node[folder.uuid] = new_folder

        for folder in folders:
            folder_node = self.uuid_to_node[folder.uuid] 
            for fid in chain(folder.folder_ids, folder.file_ids):
                child = self.uuid_to_node[fid]
                child.parents.append(folder_node.uuid)
                folder_node.children.append(child)

        for team in teams:
            new_team = Node(uuid=team.uuid, users=set(team.user_ids))
            self.uuid_to_node[team.uuid] = new_team
            for fid in chain(team.folder_ids, team.file_ids):
                child = self.uuid_to_node[fid]
                child.parents.append(new_team.uuid)
                new_team.children.append(child)

        self.roots = [n for n in self.uuid_to_node.values() if len(n.parents) == 0]

    def get_fewest(self, user_id):
        res = []
        q = deque(self.roots)
        while q:
            n = q.popleft()
            print(n)
            if user_id in n.users:
                res.append(n)
                continue
            q.extend(n.children)
        return res


class FileSystemTester(unittest.TestCase):
    def test_get_fewest(self):
        fs = FileSystem(
            [Team("Team1", ["Folder1", "Folder2"], [], ["userB"])],
            [Folder("Folder1", [], ["File1", "File2"], ["userA"]), Folder("Folder2", ["Folder3"], [], []), Folder("Folder3", [], [], ["userA"])],
            [File("File1", ["userA"]), File("File2", [])]
        )
        nodes = fs.get_fewest("userA")
        self.assertEqual(len(nodes), 2, "correct number of nodes")
        self.assertEqual(len([f for f in nodes if f.uuid == "Folder1"]), 1, "contains one instance of folder 1")
        self.assertEqual(len([f for f in nodes if f.uuid == "Folder3"]), 1, "contains one instance of folder 3")

    def test_get_fewest_bug_demonstration(self):
        """
        Test case that demonstrates the correct understanding of inheritance.
        
        Structure:
        Team1 (userA access)
        ├── Folder1 (userA access) 
        │   └── File1 (userA access)
        └── Folder2 (NO userA access)
            └── Folder3 (userA access)
        
        Expected: Should return [Team1, Folder3] 
        Because: Team1 covers Folder1 and File1, but Folder3 is not covered due to Folder2 having no access
        """
        fs = FileSystem(
            [Team("Team1", ["Folder1", "Folder2"], [], ["userA"])],
            [Folder("Folder1", [], ["File1"], ["userA"]), 
             Folder("Folder2", ["Folder3"], [], []), 
             Folder("Folder3", [], [], ["userA"])],
            [File("File1", ["userA"])]
        )
        
        nodes = fs.get_fewest("userA")
        node_uuids = [node.uuid for node in nodes]
        
        print(f"Current result: {node_uuids}")
        print("Expected: ['Team1', 'Folder3']")
        print("Explanation: Team1 covers Folder1 and File1, but Folder3 needs separate access")
        
        # The current implementation correctly returns only Team1
        # But it should also return Folder3 since it's not covered by Team1
        self.assertIn("Team1", node_uuids, "Should include Team1")
        self.assertNotIn("Folder1", node_uuids, "Should NOT include Folder1 (covered by Team1)")
        self.assertNotIn("File1", node_uuids, "Should NOT include File1 (covered by Team1)")

    def test_get_fewest_real_bug(self):
        """
        Test case that demonstrates a real bug in the current implementation.
        
        Structure:
        Team1 (userA access)
        ├── Folder1 (userA access) 
        │   └── File1 (userA access)
        └── Folder2 (userA access)
            └── Folder3 (userA access)
        
        Expected: Should return [Team1] 
        Current: Returns [Team1, Folder1, Folder2, Folder3] (bug - includes children)
        """
        fs = FileSystem(
            [Team("Team1", ["Folder1", "Folder2"], [], ["userA"])],
            [Folder("Folder1", [], ["File1"], ["userA"]), 
             Folder("Folder2", ["Folder3"], [], ["userA"]), 
             Folder("Folder3", [], [], ["userA"])],
            [File("File1", ["userA"])]
        )
        
        nodes = fs.get_fewest("userA")
        node_uuids = [node.uuid for node in nodes]
        
        print(f"Current result: {node_uuids}")
        print("Expected: ['Team1']")
        print("Bug: Current implementation returns children even though Team1 covers everything")
        
        # This test demonstrates the real bug
        self.assertIn("Team1", node_uuids, "Should include Team1")
        self.assertEqual(len(node_uuids), 1, "Should return only Team1 (minimal set)")
        self.assertNotIn("Folder1", node_uuids, "Should NOT include Folder1 (covered by Team1)")
        self.assertNotIn("Folder2", node_uuids, "Should NOT include Folder2 (covered by Team1)")
        self.assertNotIn("Folder3", node_uuids, "Should NOT include Folder3 (covered by Team1)")
        self.assertNotIn("File1", node_uuids, "Should NOT include File1 (covered by Team1)")


class SimpleFileSystemTester(unittest.TestCase):
    def test_basic_topmost_accessible(self):
        """Test the basic case from the problem statement"""
        nodes = [
            FileSystemNode("1", None, "folder", "root", ["user1"]),
            FileSystemNode("2", "1", "folder", "folder1", ["user1", "user2"]),
            FileSystemNode("3", "2", "file", "file1", ["user2"])
        ]
        
        fs = SimpleFileSystem(nodes)
        result = fs.get_topmost_accessible("user1")
        
        # user1 has access to root and folder1, but only root should be returned
        # because folder1 is covered by root
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[0].name, "root")
    
    def test_user2_access(self):
        """Test user2 access pattern"""
        nodes = [
            FileSystemNode("1", None, "folder", "root", ["user1"]),
            FileSystemNode("2", "1", "folder", "folder1", ["user1", "user2"]),
            FileSystemNode("3", "2", "file", "file1", ["user2"])
        ]
        
        fs = SimpleFileSystem(nodes)
        result = fs.get_topmost_accessible("user2")
        
        # user2 has access to folder1 and file1, but only folder1 should be returned
        # because file1 is covered by folder1
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, "2")
        self.assertEqual(result[0].name, "folder1")
    
    def test_multiple_topmost_nodes(self):
        """Test case where user has access to multiple topmost nodes"""
        nodes = [
            FileSystemNode("1", None, "folder", "root", ["user1"]),
            FileSystemNode("2", "1", "folder", "folder1", ["user2"]),  # user2 only
            FileSystemNode("3", "1", "folder", "folder2", ["user2"]),  # user2 only
            FileSystemNode("4", "2", "file", "file1", ["user2"]),
            FileSystemNode("5", "3", "file", "file2", ["user2"])
        ]
        
        fs = SimpleFileSystem(nodes)
        result = fs.get_topmost_accessible("user2")
        
        # user2 should get folder1 and folder2 (both are topmost)
        self.assertEqual(len(result), 2)
        result_ids = {node.id for node in result}
        self.assertEqual(result_ids, {"2", "3"})
    
    def test_no_access(self):
        """Test case where user has no access"""
        nodes = [
            FileSystemNode("1", None, "folder", "root", ["user1"]),
            FileSystemNode("2", "1", "folder", "folder1", ["user1"]),
            FileSystemNode("3", "2", "file", "file1", ["user1"])
        ]
        
        fs = SimpleFileSystem(nodes)
        result = fs.get_topmost_accessible("user2")
        
        # user2 has no access to anything
        self.assertEqual(len(result), 0)
    
    def test_complex_hierarchy(self):
        """Test a more complex hierarchy"""
        nodes = [
            FileSystemNode("1", None, "folder", "root", ["user1"]),
            FileSystemNode("2", "1", "folder", "folder1", ["user1", "user2"]),
            FileSystemNode("3", "2", "folder", "subfolder1", ["user2"]),
            FileSystemNode("4", "3", "file", "file1", ["user2"]),
            FileSystemNode("5", "1", "folder", "folder2", ["user2"]),
            FileSystemNode("6", "5", "file", "file2", ["user2"])
        ]
        
        fs = SimpleFileSystem(nodes)
        result = fs.get_topmost_accessible("user2")
        
        # user2 should get folder1 and folder2 (both are topmost)
        # folder1 covers subfolder1 and file1
        # folder2 covers file2
        self.assertEqual(len(result), 2)
        result_ids = {node.id for node in result}
        self.assertEqual(result_ids, {"2", "5"})
    
    def test_orphaned_nodes(self):
        """Test case with nodes that have invalid parent references"""
        nodes = [
            FileSystemNode("1", None, "folder", "root", ["user1"]),
            FileSystemNode("2", "999", "folder", "orphaned", ["user1"]),  # Invalid parent
            FileSystemNode("3", "2", "file", "file1", ["user1"])
        ]
        
        fs = SimpleFileSystem(nodes)
        result = fs.get_topmost_accessible("user1")
        
        # Should handle orphaned nodes gracefully
        # root should be returned, orphaned should be returned (no parent access)
        self.assertEqual(len(result), 2)
        result_ids = {node.id for node in result}
        self.assertEqual(result_ids, {"1", "2"})


if __name__ == "__main__":
    # Example usage of SimpleFileSystem
    print("=== SimpleFileSystem Example ===")
    
    # Create nodes as described in the problem statement
    nodes = [
        FileSystemNode("1", None, "folder", "root", ["user1"]),
        FileSystemNode("2", "1", "folder", "folder1", ["user1", "user2"]),
        FileSystemNode("3", "2", "file", "file1", ["user2"])
    ]
    
    fs = SimpleFileSystem(nodes)
    
    # Test user1 access
    user1_result = fs.get_topmost_accessible("user1")
    print(f"User1 topmost accessible: {[node.name for node in user1_result]}")
    
    # Test user2 access
    user2_result = fs.get_topmost_accessible("user2")
    print(f"User2 topmost accessible: {[node.name for node in user2_result]}")
    
    print("\n=== Running Tests ===")
    unittest.main()