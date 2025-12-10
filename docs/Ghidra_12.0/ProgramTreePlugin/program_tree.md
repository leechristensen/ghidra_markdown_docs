[Home](../index.md) > [ProgramTreePlugin](index.md) > Cut/Copy/Paste and Drag and Drop

# Program Tree


The Program Tree shows a program organized into folders and fragments. Fragments
contain code units (instructions, defined data, or undefined data). Code Units can reside in
*one and only one fragment*. A folder is a container for other folders and fragments,
however, it is not analogous to a  folder in a "file system." Any folder, except for the
root folder, and any fragment can have *multiple* parents. When you copy a folder or
fragment to another parent folder, you are not creating a new instance of the folder or
fragment, but simply adding the destination folder as another parent of the copied folder or
fragment.  This means that if you make a change to Folder "A" (e.g., create a new fragment
or folder), the change is reflected where ever Folder "A" appears in the tree, regardless of
the parent. Moving code units from one fragment to another does not affect the underlying
memory.


You can manipulate the tree organization by cutting, copying, and pasting folders and
fragments to other folders. You can also use drag and drop to reorder the contents of a folder.
You can apply algorithms to produce [organizations](Program_Organizations.md) based
on a [Block Model](../BlockModel/Block_Model.md). The following paragraphs
describe features of the Program Tree.


| ![](images/ViewManager.png) |
| --- |


## Folders and Fragments


### Create Folders and Fragments


- To create a new folder,


1. Select a folder in the Program Tree.
2. Right mouse-click, choose the **Create Folder**
option.
3. A new folder is created with the default name of "New Folder." (A one-up number is
appended to "New Folder" if that name already exists.) The cell editor for the tree is
displayed immediately so that you can change the name of the folder you just created.
Names are unique across all folders.


- To create a new fragment,


1. Select a folder in the Program Tree,
2. Right mouse-click, choose the **Create Fragment**
option.
3. A new empty fragment is created with the default name of **New Fragment**. (A
one-up number is appended to the "New Fragment" name if that name already exists.) The
cell editor for the tree is displayed immediately so that you can change the name of the
fragment you just created. Names are unique across all fragments.


> **Tip:** After you are done editing the name, the icon for the
fragment indicates that it is empty ( ). You can drag
code units from the Code Browser and drop them onto the empty node. The icon changes to
indicate that the fragment is not empty.


To create a new fragment via drag and drop,


1. Drag code units from the Code Browser.
2. Drop them onto a folder.


> **Tip:** The default name of the fragment is the name of the
first address in the set of code units that you dragged. This operation actually moves the code units to this fragment. If the first code unit in the set that you
are dragging has a label, then the name of the fragment defaults to this label
name.


### Delete Folders and Fragments


- You can delete a folder or fragment if (1) it is empty, or (2) if it exists elsewhere
in the Program at some other folder. (The delete option will be disabled if this criteria
is not met.)


To delete a folder or fragment,


1. Select a folder or fragment to delete.
2. Right mouse-click, and choose the **Delete** option.


- You can delete multiple folders and fragments; the option will be enabled if at least
one folder or fragment in the selection can be deleted; you will get an error message for
the other ones in the selection that could not be deleted.


### Rename Folders and Fragments


To rename a folder or fragment,


1. Select the folder or fragment,
2. right mouse-click, and choose the **Rename**
option.
3. The cell editor for the tree is displayed. Enter a new name.


> **Tip:** Duplicate folder or fragment names are not allowed,
regardless of where they are in the hierarchy. If you enter a name that already exists, an
error message is displayed; the name reverts back to its original name. Hit the <Esc>
key to cancel editing at any time.


### Expand/Collapse Folders


- You can recursively expand a folder. Select a folder that has subfolders; right
mouse-click and choose the **Expand All** option. All of the descendant folders are
expanded.
- Similarly, you can recursively collapse a folder. Select a folder that has subfolders;
right mouse-click and choose the **Collapse All** option. When you open the folder, you
will see that all of its descendant folders are collapsed.


### Merge a Folder with its Parent Folder


You can "flatten" a folder such that all of its immediate children are moved to the
folder's parent. For example, consider folder A that contains folder B; folder B contains
five fragments and another folder, C. You can select folder B, right mouse-click, and
choose the **Merge with Parent** option. This operation results in
the five fragments and folder C in folder B get moved to folder A. Folder B is removed.


You can make a multiple selection, however, if the selection does not contain at least
one folder, the **Merge with Parent** option is
disabled.


### Move Code Units to a Fragment


To move code units to an existing fragment,


1. Make a selection in the Code Browser.
2. Drag the selection over to a fragment in the Program Tree and drop it.


The code units are *moved* from the source fragment to the destination
Fragment.


> **Note:** Drag and drop the
selection on a folder to create a new fragment.


### Tool Tips on a Fragment


The tool tip on a fragment shows the address ranges that comprise this fragment. The
tool tip is displayed when you let the mouse pointer hover over a fragment node in the
Program Tree.


### Sort by Address or Name


You can sort the descendants of a folder by address order or by name.


To sort by address,


1. Select a folder in the Program Tree.
2. Right mouse click and choose the **Sort** → **by Address** option.


All descendants of the folder are rearranged such that they appear in address order in
the tree. This is a recursive operation.


To sort by name,


1. Select a folder in the Program Tree.
2. Right mouse click and choose the **Sort** → **by Name** option.


All descendants of the folder are rearranged such that they appear in alphabetical
order. This is a recursive operation.


*Provided By:  *ModuleSortPlugin**


### Auto Rename on a Fragment


From the Program Tree, you can automatically rename a fragment to the label at the
minimum address of the fragment.  Also, you can rename a fragment to any label in that
fragment using the pop-up menu in the code browser.


To automatically rename a fragment,


1. Select a fragment (or fragments) in the Program Tree.
2. Right mouse click and choose **Auto Rename**.


To  automatically rename a fragment to any label in
the fragment from the Code Browser,


1. Position the cursor over a label field.
2. Right mouse click and choose **Rename Fragment to Label**.


*Provided By: *AutoRenamePlugin**


### Select Addresses in a Folder or Fragment


To select all the addresses in a folder or fragment,


1. Select a fragment or module in the Program Tree.
2. Right mouse click and choose the **Select Addresses** option.
All addresses contained within the selected folders, fragments are shown in the Code
Browser's selection.


> **Tip:** This option is available for a multiple selection of
fragments and/or folders.


*Provided By: *ProgramTreeSelectionPlugin**


## Control the View in the Code Browser


The view in the code browser is controlled by the following:


### Show Folders/ Fragments in the Code Browser


You control what you see in the right side of the Code Browser tool by adding folders
and fragments to your view.


- Select a fragment that is not in the view (indicated by ![codeNotInView.gif](../icons/codeNotInView.gif)),
1. Right mouse-click and choose the **Go To in View**
option.
2. The code units in this fragment now appear in the Code Browser. The fragment's
icon in the Program Tree changes to ![codeInView.gif](../icons/codeInView.gif) to indicate
that it is part of the view. The cursor in the Code Browser is moved to the minimum
address of the fragment or folder.
- Select an open folder that is not in the view (indicated by ![openSmallFolder.png](../icons/openSmallFolder.png)),
1. Right mouse-click and choose the **Go To in View** option.
2. All of the descendant folders and fragments are added to the view.
- The folder's icon in the Program Tree changes to ![openFolderInView.png](../icons/openFolderInView.png).
- If the folder is closed and is in the view, then the icon is ![closedFolderInView.png](../icons/closedFolderInView.png).
- If a closed folder not in the view has descendants that *are* in the
view, the icon is ![closedDescendantsInView.png](../icons/closedDescendantsInView.png).
- When you add a folder to the view, the cursor in the browser moves to the first code
unit in the first fragment of the folder. When you add a fragment to the view, the cursor
in the browser moves to the first code unit in this fragment.
- You can add multiple folders and fragments to the view by selecting those folders and
fragments that you want, and choosing the **Show in View**
option.


> **Note:** The Go To in View option is always enabled
regardless of whether the folder or fragment is in the view or not.


### Remove Folders/Fragments from the view in the Code Browser


- To remove folders and fragments from the view in the code browser,
1. Select a folder or fragment that is in the view.
2. Right mouse-click, and choose the **Remove from View**
option.
- The icon for the folder or fragment updates to indicate that it is no longer in
the view. The code browser updates its view accordingly.
- You can remove multiple folders and fragments by selecting those folders and fragments
that are marked as being in the view, and choosing the **Remove from
View** option.


### Set the View in the Code Browser with Folders/Fragments


- To set the view in the code browser with folders and fragments,
1. Select a folder or fragment (or select multiple folders and fragments),
2. Right mouse-click and choose the **Set View** option. The code browser now
shows the code units for these folders and fragments.


### Add to the View in the Code Browser


- To add a folder or fragment to the view in the code browser,
1. Select a folder or fragment (or select multiple folders and fragments),
2. Right mouse-click and choose the **Add to View** option. The code browser now
shows the code units for these folders and fragments.


### Navigation


You can navigate to the first address of the code unit in a fragment by choosing the
**Go To in View** option.


- If the fragment or folder is already in the view, the code browser navigates to the
first code unit in the fragment.
- If the fragment or folder is not in the view, it is added to the view; then the code
browser navigates to the first code unit in the fragment that was added.


## Cut/Copy/Paste and Drag and Drop


### Cut and Paste


- You can move fragments and folders to other folders by cutting and pasting.


1. Select a folder.
2. Right mouse-click, and choose the **Cut** option.


The icon for the folder changes to indicate the cut operation. Choose another folder
that does not already contain this folder, right mouse-click, and choose the **Paste** option. The "cut" folder (and all of its descendants) should
now show up in the destination folder. You can select multiple folders and fragments for
cutting and pasting.


- You can merge fragments by cutting and pasting.


1. Select a fragment (or multiple fragments).
2. Right mouse-click, and choose the **Cut** option.
3. The icon for the fragment changes to indicate the cut operation; choose another
fragment.
4. Right mouse-click and choose the **Paste**
option.


The code units from the "cut" fragments are moved to the destination fragment. The
resulting empty fragments are removed from the program.


If you paste a folder or fragment not in the view to a folder that is in the view, then
the view in the code browser will be updated to show the code units for the folder or
fragment that was pasted at the destination folder.


### Copy and Paste


You can copy fragments and folders to other folders by copying and pasting.


1. Select a folder
2. Right mouse-click, and  choose the **Copy**
option.
3. Choose another folder that does not already contain this folder,
4. Right mouse-click, and choose the **Paste**
option.


The copied fragment or folder should now show up in the destination folder.


### Drag and Drop (Move)


You can get the same effect of "Cut" and "Paste" by using Drag and Drop.


Drag a folder or  fragment or to another folder and drop it. The folder or fragment
is *moved* to this folder. If the fragment or folder already exists at a folder, then
you will not get a valid drop target.


### Drag and Drop (Copy)


You can get the same effect of "Copy" and "Paste" by holding down the Ctrl key while
dragging. (If you release the Ctrl key, the drag operation becomes a Move.)


Drag/Copy a folder or fragment to another folder; the cursor changes to indicate the
copy operation. Drop the folder or fragment; a copy is made and placed in the destination
folder.


As stated earlier, you can drag code units from the Code Browser view and drop them onto
a folder (creates a new fragment), or onto an existing fragment (moves the code units to
this fragment).


If you try to drag/copy a folder or fragment to a folder that already contains the
folder or fragment, you will not get a valid drop target.


### Reorder Folder Contents using Drag and Drop


- Using Drag and Drop, you can reorder the elements within a folder. As you drag between
nodes in the Program Tree, the cursor will change to indicate that a reordering
operation  is possible; you will see a solid bar between the nodes (![dragMoveCursor.gif](../icons/dragMoveCursor.gif)). When you release the mouse, the dragged folder or fragment
will be repositioned at this location, i.e., *between* the two nodes where you
released the mouse.
- If you are dragging to a different parent,  in addition to the reorder, the
drop operation will also cause the dragged fragment or folder to be ***moved*** to
the parent of the destination drop site. To make a copy of the folder or fragment, hold
down the Ctrl key while you are dragging. The cursor will change to ![dragCopyCursor.gif](../icons/dragCopyCursor.gif) depending on where the cursor is.  If you release the
mouse when the cursor indicates a potential reorder operation, the dragged folder or
fragment is ***copied*** to the ***parent*** of the destination drop site,
and is placed between the two nodes where you released the mouse. (Note that if the dragged
folder or fragment already exists in the parent, then you will not get a valid drop target
for reordering purposes.)


### Menu Enablement


If you select multiple nodes in the Program Tree, some menu items in the popup menu
(right mouse click) may not be enabled if the multi-selection is not valid. A valid
multi-selection meets the following criteria:


- If a folder is selected, then either all of its immediate descendants must be
selected, or none of its immediate descendants is selected.
- The root folder is not part of the selection.


A valid multi-selection will cause the **Copy**, **Cut**, **Delete**, and view options to be
enabled.


The **Delete** option may be enabled for a multi-selection,
however, if the delete operation is not allowed on a particular folder or fragment, you
will get a notification of why the delete failed.


*Provided By: *Program Tree Plugin**


**Related Topics:**


- [View Manager](view_manager.md)
- [Program Organizations](Program_Organizations.md)
- [Code Browser](../CodeBrowserPlugin/CodeBrowser.md)


---

[← Previous: Control the View](program_tree.md) | [Next: Program Organizations →](Program_Organizations.md)
