[Home](../index.md) > [ScalarSearchPlugin](index.md) > Scalars

# Search for Scalars


Search for Scalars locates scalar operands and values in the current program.  The search is
based on a value entered as hex or decimal numbers. The scalar can be in
instructions, data, or structures.


## To Search for Scalars:


1. From the Tool, select **Search** →  **For
Scalars...**
2. Select "Scalars in Range:" or "Specific Scalar:".
3. Once the search type is selected, enter scalars into the value fields in either decimal
or hexadecimal (0x...) notation.
4. Choose "Search" to begin the search.


> **Tip:** Once a value is entered in a
text field, Ctrl+M toggles the value display between the
decimal and hex 	representation of the value in that field.


![](images/SearchAllScalarsDialog.png)


## Search Options


### Search Type


#### Scalars in Range


Search the program for all scalars within the given range.


#### Specific Scalar


Search the program for all instances of one scalar value.


### Selection Scope


#### Search All


The search will search all memory in the program.


#### Search Selection


The search will be restricted to the current selection in the tool. This
option is only enabled if there is a selection in the tool.


## Scalar Table


After the user begins a scalar search, the plugin will display a results table to the
user. The table shows the address of the scalar, a preview of the item at that address, the
scalar in Hex, and the scalar in signed decimal as shown in the image below:


![](images/ScalarWindow.png)


Each element of the table is a scalar found in either data or an instruction in the
program.  Any new code units containing scalars added to the program will
automatically appear in the table.


To bring up the **Scalar Table**, choose **Window** → **Scalar Table** from the tool's menu. This table can be docked in the tool
if desired.


The Scalar Table contains the following default columns:


- **Location** - displays the address of the code unit containing the scalar.
- **Preview** - displays the code unit containing the scalar.
- **Hex** - displays the scalar as an unsigned hex number.
- **Decimal (Signed)** - displays the scalar as a decimal number.
- **Function Name** - displays the name of the function containing the scalar.
- **Decimal (Unsigned)** - displays the scalar as a decimal number (this
column is hidden by default).
- **Bits** - displays the number of bits required to store the scalar value (this
column is hidden by default).
- **Signedness** - displays whether the scalar is *signed* or *unsigned* (this
column is hidden by default).


## Scalar Table Filters


The scalar table has the following
[filters](../Trees/GhidraTreeFilter.md) at the bottom of the table:


1. **Text Filter** - allows you to filter based on any text in the table.
2. **Range Filter** - allows you to filter on a range of scalars **based
upon their signed value**.
3. **Column Filter** - allows you to filter on specific column values.


## Actions


### Make Selection


*See [Make Selection](../Search/Query_Results_Dialog.md#make-selection)*


### Selection Navigation


*See [Selection Navigation](../Search/Query_Results_Dialog.md#selection-navigation)*


### Remove Items


*See [Remove Items](../Search/Query_Results_Dialog.md#remove-items)*


*Provided by: *ScalarTablePlugin**


---

[← Previous: Strings](../Search/Search_for_Strings.md) | [Next: Instruction Patterns →](../Search/Search_Instruction_Patterns.md)
