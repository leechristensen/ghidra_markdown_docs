[Home](../index.md) > [Search](index.md) > Instruction Patterns

# Instruction Pattern Search


This dialog allows users to search the current program for specific instruction sequences.
Operands and mnemonics may be masked to allow maximum flexibility in modifying the search
pattern.


![](images/SearchInstructionPatterns.png)


## **Dialog Layout**


The search dialog consists of two main components: the *Instruction Table* and the
*Preview Table*. The former contains all instructions selected by the user; the latter
displays the string (in binary or hex) that will be used for searching


### Instruction Table


![](images/SearchInstructionPatternsInstructionTable.png)


This table is populated when a selection is made in the code listing and the ![reload.png](../icons/reload.png) icon is selected. All items in
the selection range will have an entry in the table, even non-instructions. Users may click
on an item in the table to mask it from the final search string.


> **Tip:** Color-coding is used to indicate the code
unit type. Instructions are displayed in
blue , data items are tan .


#### Instruction Table Toolbar


![](images/SearchInstructionPatternsInstructionTableToolbar.png)


These tools provide ways to manipulate the Instruction Table and are discussed in
detail below:


- [ ![Clear](../icons/erase16.png) ] Clears
all masks.
- [ ![Undefined](../icons/DOSA_D.png) ] Masks all
data (non-instructions).
- [ ![Operand](../icons/DOSA_O.png) ] Masks all
operands.
- [ ![Scalar](../icons/DOSA_S.png) ] Masks all
scalar operands.
- [ ![Address](../icons/DOSA_A.png) ] Masks all
address operands.
- [ ![Refresh](../icons/reload3.png) ] Reloads the
table from what is currently selected in the listing.
- [ ![Add](../icons/Plus2.png) ] Add to the table what is currently
selected in the listing.
- [ ![Entry](../icons/editbytes.gif) ] Allows
users to manually enter bytes to be loaded.
- [ ![Home](../icons/go-home.png) ] Navigates in
the listing to the location defined by this set of instructions.


### Preview Table


![](images/SearchInstructionPatternsPreviewTable.png)


The Preview Table shows what the search string will look like, in either binary or hex
format. It will change dynamically as masks are applied/removed in the Instruction Table.


- When viewing the table in binary mode, any masked bits will appear as periods
[**.**]
- In Hex mode, if any part of a byte has masked bits, the hex value will not be shown;
instead, the binary value with the masked bits will be displayed inside brackets. ie:
**[001..011]**


#### Preview Table Toolbar


![](images/SearchInstructionPatternsPreviewTableToolbar.png)


These tools provide ways to manipulate the Preview Table and are discussed in detail
below:


- [ ![binaryData.gif](../icons/binaryData.gif) ] Switches to
binary display mode.
- [ ![hexData.png](../icons/hexData.png) ] Switches to
hex display mode.
- [ ![page_white_copy.png](../icons/page_white_copy.png) ] Copies the
preview table contents to the clipboard.


### Search Bounds


By default any search will be run against the entire program. If you only want to search a
particular range, that can be done using the options below:


![](images/SearchInstructionPatternsControlPanel.png)


- Selection Scope
- Allows the user to specify what region of the program will be searched. The default
is to search for the entire program. If *Search Selection* is chosen, whatever
region is currently selected in the listing will be used as the search bounds.
- Search Direction
- Indicates whether subsequent invocations of the *Search* button will look
forward or backward in the listing for the search pattern.


### Manual Entry


![](images/SearchInstructionsManualSearchDialog.png)


If the user clicks the ![editbytes.gif](../icons/editbytes.gif)
button, the manual entry dialog above will be displayed. Users may enter either a binary or
hex string here (full bytes, no nibbles!) and if the string represents a valid set of
instructions for the loaded program, then activating the *Apply* button will cause them
to be displayed in the *Instruction Table*.


### Search Results


If the user clicks the *Search All* button, all search results will be shown in a
single window, where each entry represents the starting address of a match. Clicking on an
entry will take you to that spot in the listing.


If the user clicks the *Search* button, no results table will appear but the cursor
will immediately move to the next match in the listing. Whether the cursor moves to the next
or previous match depends on the *Search Direction* setting.


![](images/SearchInstructionPatternsResultsTable.png)


> **Tip:** It should be noted that the search will look
for exact byte pattern matches, not simply the mnemonic and/or operand text. eg: If you load a
program and select a RET instruction, you can't expect to use that same search pattern
to find a RET instruction in a different program. Unless they represent the same
architecture, their byte representations will likely be different.


## **Usage**


The most basic usage of the search dialog is as follows:


1. Select a range of instructions in the code listing.
2. From the Tool, select **Search** →  **For
Instruction Patterns**.
The dialog will launch and be populated with the instruction set.
3. Select/deselect items in the table to mask the desired instructions.
4. Click the *Search All* button. A dialog will pop up showing all occurrences of the
pattern in the program.


#### Saving a Search Pattern


Users may copy and save the generated search pattern by right-clicking on the preview
table and selecting one of the options; the text will be copied to the clipboard.


#### Constraints


- The number of instructions that can be used in a pattern is capped at **500**.
- Only one range of addresses may be selected in the code browser. MULTIPLE SELECTIONS
ARE NOT ALLOWED.


#### Multiple Programs


The instruction search dialog will always operate on the program currently selected in
the listing. If you select a set of instructions in Program A, then switch over to Program
B and select the *Search* button, Program B will be searched for the selected
instructions.


*Provided by: *InstructionSearchPlugin**


---

[← Previous: Scalars](../ScalarSearchPlugin/The_Scalar_Table.md) | [Next: Address Tables →](Search_for_AddressTables.md)
