[Home](../index.md) > [Search](index.md) > Address Tables

# Search for Address Tables


The **Search for Address Tables** feature searches the program for possible [address tables](../Glossary/glossary.md#addresstable). The search can span
the entire program or be limited to a selection. The results are presented in list form,
allowing the user to make tables and disassemble the addresses in those tables.


| ![](images/SearchForAddressTables.png) |
| --- |


### Searching for Address Tables


To search for address tables,


1. Select the **Search → For Address Tables...** option
2. Select the **Search** button; the results of the search are displayed in the table.


#### Search Options


- **Search Selection** - limit the search to the
current selection in the Listing. (The checkbox is disabled if there is no
selection).
- **Minimum Length** - determines the shortest length of the possible
address tables to display.
- **Alignment** - the address tables must be aligned on the
indicated byte boundary. For example, 2 indicates alignment on a word boundary.
- **Skip Length** - the number of bytes to skip between address matches.  This
is useful when finding addresses in structures that are known to have
non-address byte sequences between the addresses.


> **Tip:** For very large Programs
that may take a while to search, you can cancel the search at any time by hitting the cancel
( ) button. A progress bar is
displayed as needed.


### Search Results Table


Default columns:


- **Location** - location of the possible address table
- **Label** - primary label at the location of the possible table.
- **Data (Hex/Ascii)** - Ascii and hex views of the bytes pointed to by the first
element in the table.
- **Length** - the length of the possible address table


### Making Address Tables


To make an address table,


1. Select one or more rows in the **Possible Address Tables** table.
2. Select the **Auto Label** checkbox to automatically create labels at the beginning
of each address table that was created, at all of the addresses contained in those tables,
and at the top of the indexes to the tables if there are any.
3. If necessary, enter an offset (number of addresses to be skipped) to be added to the
starting address(es) (offset multiplied by 4, the address size).
- For one address table, the entered offset cannot be greater than one less than the
length of the possible table.
- For multiple address tables, the offset value cannot be greater than one less than
the length of the smallest selected table.
- The field next to *Offset* shows the adjusted start address for the table;
this field cannot be edited. It is empty for multiple table selections.
4. Select the **Make Table** button.
5. An address table gets created at the location you chose, containing defined addresses
which now point to the address created. These addresses now contain XREFs to the table
entries. If an index to the table exists immediately after the table, it will get created
as an array of bytes, as well.


> **Warning:** A warning dialog is
displayed if address tables could not be created due to a collision with existing data at
either the start of end of possible address tables. If the auto label option is selected, you
can determine from the label column those address tables that were not created.


To disassemble the address tables,


1. Select one or more rows in the **Possible Address Tables** table.
2. Select the **Disassemble** button; disassembly will begin at each address in the
selected address tables.


## Actions


### Make Selection


*See [Make Selection](Query_Results_Dialog.md#make-selection)*.


### Selection Navigation


*See [Selection Navigation](Query_Results_Dialog.md#selection-navigation)*.


*Provided by: *AutoTableDisassemblerPlugin**


**Related Topics:**


- [Search Memory](Search_Memory.md)
- [Search Program Memory](Search_Memory.md)
- [Search Program Text](Search_Program_Text.md)
- [Searching](Searching.md)


---

[← Previous: Instruction Patterns](Search_Instruction_Patterns.md) | [Next: Direct References →](Search_for_DirectReferences.md)
