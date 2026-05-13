[Home](../index.md) > [FileSystemBrowserPlugin](index.md) > FileSystem Browser

# FileSystem Browser


## Introduction


The file system browser is a generic tool for browsing and accessing the contents of
filesystems or container files (such as zips, tars, firmware images, etc).


## GHIDRA Tool File Menu Actions


### Open File System


Opens a file system container file (ie. a zip, tar, iso, etc) in a new browser tree.

Subdirectories of your local computer's file system can also be opened in this manner.


## Right-click Context Menu Actions


### Get Info


Returns information about the selected file. Sometimes there will not be any available
information. Generally, this information is not that useful. It will mostly consist of
meta-data from the internal file system.


### Expand All


Expands all folders below, and including, the selected node.


### Collapse All


Collapses all folders below, and including, the selected node.


### Open File System


Attempts to open the selected file as a sub-file-system. If this operation succeeds, the
node will turn into a folder with one or more children. If this operation fails, the node
will remain a leaf node. This operation could fail for many reasons, but generally it fails
because the node does not represent a valid sub-file-system.


### Open File System in new window


Attempts to open the selected file as a sub-file-system. If this operation succeeds, a
new file system browsing tree will be shown with the contents of the selected file.


### Open Program(s)


Opens the GHIDRA program(s) that correspond to the selected file(s). If no program in
the current GHIDRA project is linked to the selected file, you will be able to import the
selected file.


### Import


Imports the selected file into GHIDRA as new program in your current project.


### Batch Import


Imports the selected file(s) into GHIDRA as new programs in your current project
using the Batch Import dialog.


### Add To Program


Adds the selected file into the currently active program.


### Export


Writes a copy of the selected files to a directory you select on your local
computer.


### Export All


Recursively copies the contents of a selected folder to a directory you select on your
local computer.


### Add Library Search Path


Adds the currently selected file or folder to the list of library search paths which
is used during program import.


### View As Image


Attempts to render the selected file as an image.


### View As Text


Attempts to render the selected file as an text.


### List Mounted File Systems


Displays a list of the file systems that are currently open and mounted. Selecting one
of the file systems will display that file system's browser tree.


### Clear Cached Passwords


Clears any cached passwords that previously entered when accessing a password
protected container file.


### Refresh


Refreshes the status of the selected items.


### Close


Closes the currently highlighted file system root node. The file system itself will not
be unmounted until all open browser windows to it are closed and a caching timeout period
has passed.


## Browser Dialog Actions


### Open File System Chooser


Opens a new file system container file in a new browser tree. This is the same as "File
| Open File System" in the main GHIDRA window.


## Password Dialog


This dialog is used to prompt for a password when opening a password protected container.


If the password isn't known, the **Cancel** button will stop Ghidra from re-prompting
for the password for the current file during the current operation (but the user may be
re-prompted again later depending on the logic of the operation), and **Cancel All**
will stop Ghidra from prompting for passwords for any file during the current operation.


Passwords can also be provided via a text file specified on the java command line, useful
for headless operations.  See **ghidra.formats.gfilesystem.crypto.CmdLinePasswordProvider**


## How To Handle Unsupported File Systems


If you receive this message: **No file system provider for the selected file.**


It means one of the following two things:


1. The file you attempted to open as a file-system is actually NOT a file-system
2. GHIDRA does not have an implementation for that file-system


If the file does not really represent a file system, then you may want to try importing
it.


Otherwise new file-systems can easily be written by implementing the
`ghidra.formats.gfilesystem.GFileSystem` interface.


## Known issues


### Strong Crypto Support


Your Java JVM install may not have support for strong crypto currently installed.


In order to fix this issue, you must install Oracle's "Java Cryptography Extension (JCE)
Unlimited Strength Jurisdiction Policy Files"


---

[← Previous: Configuration Options](../OverviewPlugin/Overview.md) | [Next: Function Bit Patterns Explorer →](../FunctionBitPatternsExplorerPlugin/FunctionBitPatternsExplorerPlugin.md)
