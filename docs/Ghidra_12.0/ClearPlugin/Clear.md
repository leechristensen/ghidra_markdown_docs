[Home](../index.md) > [ClearPlugin](index.md) > Clear

# Clear


## Clear Code Bytes


Clear Code Bytes reverts [disassembled](../DisassemblerPlugin/Disassembly.md) instructions and [defined data](../DataPlugin/Data.md) to their undefined state. It can also be
used to clear the components of an applied structure directly from the browser.


To Clear a single instruction,


1. Position the cursor on a defined instruction or data code unit
2. From the right-mouse pop-up menu over the Code Browser window, select *Clear Code
Bytes*
Alternately: press the 'C' key


To Clear an area,


1. Select the defined code units (data and instructions)
2. From the right-mouse pop-up menu over the Code Browser window, select *Clear Code
Bytes*
Alternately: press the 'C' key


To Clear components of a structure directly in the browser,


1. Select the structure elements in the open structure
2. From the right-mouse pop-up menu over the Code Browser window, select *Clear Code
Bytes*
Alternately: press the 'C' key
3.


> **Note:** Clearing bytes
inside a structure from the CodeBrowser, changes the definition of the structure and will
affect all occurences of the structure.


## Clear With Options


*Clear With Options* more selectively clears information defined in the program.
While *Clear Code Bytes* only clears instructions and data, Clear With
Options can selectively choose either instructions or data and additionally can remove
other program information, e.g., symbols, references, functions, etc.


The *Clear* dialog has check boxes for each type of information that can be cleared.
If the check box is selected, that item will be removed everywhere within the selection when
the OK button is pressed.


![](images/ClearWithOptions.png)


To Clear With Options,


1. Create a selection in the Code Browser containing instruction and/or defined data to
be cleared.
2. From the right-mouse pop-up menu over the Code Browser window, select *Clear With
Options...*
3. De-selected the check boxes from the items that should not be cleared.
4. Click *OK*.


You
can undo clearing of code units if it has an undesired effect.


The following paragraphs describe each option.


### Symbols


Any User defined [symbol](../SymbolTablePlugin/symbol_table.md) in
the program. Automatically generated symbols won't be cleared if references still exist to
the symbol's defined address.


> **Note:** This option
will not clear function names. To delete these you must select the functions option.


### Comments


Clears Pre, Post, End of Line (EOL), Plate [comments](../CommentsPlugin/Comments.md). It will not clear comments on
functions or function variables.


> **Note:** This option
will not clear repeatable or automatic comments. To delete those comments you must
delete the associated reference.


### Properties


Properties are placed at addresses in a program by plugins to store information. This
information is usually only understood by the plugin that placed it there or other
cooperating plugins.


> **Tip:** Select the properties icon ( ) on the tool bar to display all the
properties that are currently in the program.


### Instructions


Instructions are cleared.


### Data


Defined Data elements are cleared.


### User-defined References


Any references added by the user are cleared.


### Analysis References


Any references created by analysis tasks are cleared.


### Import References


Any references created during the import process are cleared, such as calls to external
library functions.


### Default References


References automatically created by Ghidra during disassembly are cleared. This includes
references to stack variables within the body of a function.


### Functions


Defined functions are cleared, including comments and any defined variables. Any
references to stack variables within the body of the function will be cleared as well.


### Registers


Registers within the selection with a defined value will be cleared and set to
undefined. Registers can be set to a value using Set Register Values.


### Equates


Instructions with Scalar Operands set to display an alternate string with an [Equate](../EquatePlugin/Equates.md) are cleared.


### Bookmarks


All types of [Bookmarks](../BookmarkPlugin/Bookmarks.md) are
cleared.


## Clear Flow and Repair


*Clear Flow and Repair* is intended to be used to clear and optionally repair code
which was produced in error. The duration of this action will vary depending on the extent of
the instruction flow. If good code with extensive flow is encountered, the action may take a
long time to complete. If the flow analysis is lengthy, a task dialog will be displayed with
a *Cancel* button. The *Cancel* button may be pressed to terminate the action.


> **Note:** You can undo clearing of code
units if it has an undesired effect


The *Clear Flow* options dialog has check boxes to control its behavior. Pressing the
*OK* button will begin the clear process using the selected options.


| ![](images/ClearFlow.png)   |
| --- |


To Clear instructions produced by an invalid fall-through or bad code produced by a data
reference:


1. Click on the first bad instruction
2. From the right-mouse pop-up menu over the Code Browser window, select *Clear Flow
and Repair...*
3. Choose the desired *Clear Flow Options*.
4. Click *OK*.


To Clear instructions referenced by one or more pointers :


1. Select all pointer data units
2. From the right-mouse pop-up menu over the Code Browser window, select *Clear Flow
and Repair...*
3. Choose the desired *Clear Flow Options*.
4. Click *OK*.


Note that clearing pointer referenced code will also clear all computed flow references to
the address(es) referenced by the selected pointer(s).


The following paragraphs describe each option.


### Clear Symbols


All non-default [symbols](../SymbolTablePlugin/symbol_table.md) at
cleared code unit locations will be removed.


### Clear Data


All data whoose only references were from cleared code unit locations will also be
cleared.


### Repair


Following the clearing of the flow, attempt to repair the disassembly of references into
the cleared region.


*Provided By: *ClearPlugin**


**Related Topics:**


- [Disassembly](../DisassemblerPlugin/Disassembly.md)
- [Importing Files](../ImporterPlugin/importer.md)
- [Property Viewer](../PropertyManagerPlugin/Property_Viewer.md)


---

[← Previous: Bookmarks](../BookmarkPlugin/Bookmarks.md) | [Next: View Properties →](../PropertyManagerPlugin/Property_Viewer.md)
