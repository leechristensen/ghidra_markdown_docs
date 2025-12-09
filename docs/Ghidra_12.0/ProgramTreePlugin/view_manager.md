[Home](../index.md) > [ProgramTreePlugin](index.md) > Close view

# Program Tree View Management


Program Trees are used to organize programs into a tree structure. Nodes within the a
program tree can be used to navigate to the corresponding address in the [Code Browser](../CodeBrowserPlugin/CodeBrowser.md). Also, the program tree can be
used to restrict the view (set of addresses) that are displayed in the [Code Browser](../CodeBrowserPlugin/CodeBrowser.md). The Program Tree Manager allows you to [create](#create-default-tree-view) , [delete](#delete-tree-view), [rename](#rename-tree-view), and [close](#close-tree-view) program tree
views.


| ![](images/ViewManager.png) |
| --- |


The following paragraphs describe features of the Program Tree Manager.


### Create a Default Program Tree


A default tree has a fragment for each memory block in the program; the fragments are
named the same as the memory blocks.


When you bring up a Code Browser, the Program Tree Manager (the tabbed pane on the left
side of the Code Browser) shows a default view with no program open. When you open a program,
the Program Tree Manager will create a tab for each tree view that is in the
program. When you re-open the project, the Program Tree Manager will show the view from
when you last closed the project.


You can create a new default program tree by selecting the ![layout_add.png](../icons/layout_add.png) icon. A new tab is displayed with
the default name of the view, "Program Tree." If a view named "Program Tree" exists, then the
name has a one-up number appended to it to ensure the name is unique, e.g., "Program
Tree(1)."


*Provided by: *ProgramTreePlugin**


### Open Program Tree


You can see a list of existing Program Trees in the Program by selecting the ![preferences-system-windows.png](../icons/preferences-system-windows.png) icon. Select
the program tree name from the popup menu; a tab is created in the panel for this tree, if
one does not already exist. The selected tree becomes the current tree in the tabbed
pane.


*Provided by: *ProgramTreePlugin**


### Select Fragments Corresponding to a Program Location


The icon  ![locationIn.gif](../icons/locationIn.gif)
is a toggle button that controls whether the fragment(s) that correspond to the location in
the code browser should be selected in the Program Tree.  **On** means to select the
fragment(s) that contain the address of the location. While the button is **On**, the
Program Tree will track the location in the browser by selecting the appropriate
fragments.  The toggle is **Off** by default.


*Provided by: *ProgramTreePlugin**


### Close a  Program Tree


To close a program tree, right-mouse click on the tab of that program tree and choose the "Close" option.
Closing a program tree does not affect the Program.


Re-open the program tree by selecting it from the list of views described above.


> **Note:** You cannot close the
last program tree..


### Rename a  Program Tree


To rename a program tree,


1. Right-mouse click on the tab of the program tree.
2. Choose the "Rename" option.
3. A text field is created over the tab; the value defaults to the current view name and
is selected. Enter a new name.


If another view exists with this name, a message is displayed in the status area of the
tool. The list of existing views will show the new name.


> **Note:** If you move focus out
of the edit window, the edit window is removed, and no change is made to the name.


Click the ![Undo](../icons/edit-undo.png) button to
undo the rename.


### Delete a Program Tree


To delete a program tree,


1. Right-mouse click on the tab of the program tree.
2. Choose the "Delete" option.


> **Note:** You cannot delete the
last program tree. You must first create a new default tree, then delete your other tree.


Click the ![Undo](../icons/edit-undo.png) button to
undo the Delete.


### Change to Other Program Tree


To switch to another tree view, either click on another tab, OR select a program tree name
from the list of program trees.


*Provided By: *View Manager Plugin**


Related Topics:


- [Program Tree](program_tree.md)
- [Program
Organizations](Program_Organizations.md)
- [Code Browser](../CodeBrowserPlugin/CodeBrowser.md)


---

[← Previous: Rename view](view_manager.md) | [Next: Program Validator →](../ValidateProgram/ValidateProgram.md)
