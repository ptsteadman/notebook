"""
Shell tab autocompletion

The entire problem is set in the context of the Linux shell's tab auto-completion feature.
First Question: Given a series of files ["file1", "file2", "file_new"] and the input "f", the task is to return the auto-completion result ("file"), which is the longest common prefix of all files matching the current input.
Second Question: The files may be located in subfolders ["folder/file1", "folder/file2", "folder/file/new"]. The input does not include "/". The expected output is the auto-completion result ("folder/file"), with the requirement that if all files matching the current input are in the same folder, the shell should automatically enter that folder.
Third Question: The input may include "/".
"""
