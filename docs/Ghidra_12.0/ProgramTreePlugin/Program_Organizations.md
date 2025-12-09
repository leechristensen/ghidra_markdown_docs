[Home](../index.md) > [ProgramTreePlugin](index.md) > Program Organizations

# Program Organizations


You can automatically organize the structure of a Program by applying subroutine algorithms
to folders and fragments. The new organization is reflected in the [Program Tree](program_tree.md).


## Subroutine Modularization


This partitions the Program into subroutines that are all based on a specific [Block Model](../BlockModel/Block_Model.md); the algorithm is summarized as
follows:


1. Use the selected block model to gather the code blocks that overlap the address set of
the selected folder or fragment.
2. For each code block create a new folder; use the code block name as the name of the
folder.
- If you selected a folder to modularize, new folders are created under the selected
folder.
- If you selected a fragment to modularize, a new folder is created using the
fragment name. Folders for the code blocks are created under this folder.
3. For each code block from Step 2, use the selected block model to gather code blocks
that overlap the address set of the code block.
4. For each of these code blocks from Step 3 create a new fragment; use the block name as
the name of this fragment.
5. Move the code units in the code block to the new fragment.
6. Update the names of folders to include the number of elements (folders and fragments)
the folder contains.


To organize a folder or fragment by modularization and block model, right mouse click on a
folder or fragment in the [Program Tree](program_tree.md) and choose **Modularize By** → **Subroutine** → ***`<block model name>`.***


*Provided by: *ModularizeAlgorithmPlugin**


## Dominance Tree Modularization


This action modularizes the program tree by creating a call tree of the
code blocks and then arranges that tree by dominance such that all blocks only
reachable from a parent `'p'` are children of `'p'` in the program tree.


## Complexity Depth Modularization


This action modularizes the program tree by placing code blocks in a folder that marks the
longest possible call tree path that calls that block.  For example, blocks
at `Level 0`
are not called by any other code; blocks at `Level 30` are blocks that have
a call tree path to them that contains 30 nodes.  Note that the nodes at `Level
30` may have shorter paths that reach them, but the longest of all the paths
is 30 nodes.


You can cancel the organization process at any time using the progress bar. Whatever
fragments or folders that were generated up to the point when you canceled the operation will
remain in the tree. Click on the ![Undo](../icons/edit-undo.png)button to undo the
organization changes.


## Default Tree Organizations


When you [import a Program](../ImporterPlugin/importer.md) or [create a new
tree](view_manager.md#create-default-tree-view), a *default tree organization* is created; a fragment is created for each of
the memory blocks. The fragment name is the same as the memory block name.


*Provided by: *ProgramTreePlugin**


**Related Topics:**


- [Create a Default View](view_manager.md)
- [Block Models](../BlockModel/Block_Model.md)
- [Import a Program](../ImporterPlugin/importer.md)
- [Program Tree](program_tree.md)


---

[← Previous: Cut/Copy/Paste and Drag and Drop](program_tree.md) | [Next: Create view →](view_manager.md)
