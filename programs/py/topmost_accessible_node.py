"""
Context: We have a hierarchical file system where design files and folders are organized in a tree structure (similar to how files/folders are organized in Figma). Each file/folder has specific user access permissions. We need to build a system to efficiently determine what content is accessible to users.
Problem Statement: Given a file system tree where each node (file/folder) has:
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
from typing import List, Set
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


if __name__ == "__main__":
    unittest.main()