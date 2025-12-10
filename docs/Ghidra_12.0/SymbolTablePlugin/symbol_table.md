[Home](../index.md) > [SymbolTablePlugin](index.md) > Symbol Table

# Symbol Table


The *Symbol Table* displays a tabular view of each symbol currently defined in the
program.


A symbol, also known as a label, is an association between a name and an address.


## **Displaying the Symbol Table component**


- From the menu-bar of a tool, select **Window  →  Symbol
Table**
- From the tool-bar of a tool, click on the ![table.png](../icons/table.png) button


![](images/Symbol_Table.png)


Some of the columns in the table are:


| **Label** | Name of symbol. |
| --- | --- |
| **Location** | Address where the symbol is defined. |
| **Type** | Symbol type (Function, External, Class, etc). |
| **Namespace** | Namespace of the symbol; i.e., the scope. |
| **Source** | Indicates where the symbol name came from. |
| **Reference Count** | Total number of references made to this symbol. |


*You can sort the table on any column by clicking on
the column header. The column can be sorted in ascending or descending order.*


> **Warning:** Sorting a column in the symbol table when the program has a large number of symbols
can be slow.  If you do not need sorting, then you can control-click the sorted column
to remove the sort.


> **Tip:** The colors for bad
references , entry points , dead code , offcut code , function
names , local symbols , primary and non-primary symbols
correspond to the colors used in the Code Browser. Any changes you make to these colors
through the Code Browser
Display options will be reflected in the Symbol Table.


## Filter Text Field


The filter text field allows you to filter the list of symbols. By default it will do a
**"Contains"** filter, but you can change that behavior to be **"Starts With"**,
**"Matches Exactly"**, or **"Regular Expression"**. See [Filter Options](../Trees/GhidraTreeFilter.md#ghidra-tree-and-table-filters) for more details on the
various filter text strategies.


The *Name Only* checkbox allows you to toggle whether to filter on only the name
column or all the columns in the table.


> **Tip:** Filtering the symbol table when the program has a large number of symbols can be slow.
When only filtering on the symbol name, via the checkbox above, the overall filtering
is considerably faster.


The filter text field will accept basic globbing characters such as '*****' and
'**?**' within the filter text unless the "Regular Expression" filter strategy is
selected, in which case you should use standard regular expression syntax.


## Viewing Symbol References ![table_go.png](../icons/table_go.png)


See [Symbol References](symbol_references.md)


## Deleting Symbols ![edit-delete.png](../icons/edit-delete.png)


You can use the *Symbol Table* to delete symbols from the program.


To delete symbols:


1. Select the symbols in the Symbol Table (hold the `<Ctrl>` key down to add to the
selection) to be deleted.
2. Right-mouse-click and select "Delete" from the popup menu, or click the ![edit-delete.png](../icons/edit-delete.png) button in the *Symbol Table* toolbar.


*Notes on deleting a symbol:*


1. *You can only delete a default symbol when it has zero (0) references.*
2. *If you delete a user-defined symbol with references, then a default symbol will
automatically be created and assigned those references.*
3. *You can delete a non-primary symbol with references, but those references will be
reassigned to the primary the symbol.*


## Making a Selection ![Make Selection](../icons/stack.png)


You can make a selection that corresponds to the symbol addresses that are selected in the
*Symbol Table*.


To make a selection:


1. Select the symbols in the Symbol Table (hold the `<Ctrl>` key down to add to the
selection) to be added to the selection.
2. Right-mouse-click and select "Make Selection" from the popup menu.
  - Or, click the ![Make Selection](../icons/stack.png)  button in the *Symbol
Table* toolbar.


## Making a Selection ![Make Selection](../icons/stack.png)


When selected, the Symbol Table will select the row in the table that corresponds to the
symbol selected in the [Listing](../CodeBrowserPlugin/CodeBrowser.md).


## Renaming a Symbol


You can use the *Symbol Table* to rename a symbol.


To rename a symbol:


1. In the Symbol Table, double-click in the "Label" field on the row of the symbol to be
renamed
2. The field will become editable
3. Enter a new name and press return
4. The new name for the symbol should display in the table and Code Browser
5. If the table is being sorted on the "Label" field, then the new name should be sorted
into the table and the selection should move accordingly


## Edit External Location


You can edit the external location and associated library details for any *External Data* or
*External Function*
symbol within the symbol table.
Right mouse click on
the symbol table row and choose the **Edit External
Location** action from the popup menu (see Symbol Tree -
[Edit External Location](../SymbolTreePlugin/SymbolTree.md#edit-external-location)
for more discussion on the use of the edit dialog).


## Pinning a Symbol


Code, data, or function labels may be pinned which keeps then from moving to a new address in the
event of a memory block move or an image base change.


To pin a label:


1. Select the symbols to be pinned in the Symbol Table (hold the `<Ctrl>` key down to add to the
selection) to be added to the selection.
2. Right-mouse-click and select "Set Pinned" from the popup menu.


To unpin a label:


1. Select the symbols to be unpinned in the Symbol Table (hold the `<Ctrl>` key down to add to the
selection) to be added to the selection.
2. Right-mouse-click and select "Clear Pinned Symbol(s)" from the popup menu.


## Filtering


The list of displayed symbols is determined by the current symbol table settings. These
settings can be adjusted by clicking the *Filter* ![Configure Filter](../icons/exec.png)
button in the toolbar of the *Symbol Table* window or from the right-mouse popup menu..
The displayed symbols will correspond to the selected checkboxes in the *Symbol Table
Filter* dialog.


*Symbol Table Filter* Dialog


![](images/Filter.png)


The Symbol Table Filter dialog consists of three sets of filters - Symbol
Source, Symbol Types, and miscellaneous *[Advanced
filters](#filtering)* which are not initially shown.  The Symbol Types are further divided
into label symbols and non-label symbols.  This grouping is for informational purposes
only. For most situations, only the Source and Type filters need to be set.  This will
generate a query that will include all symbols that have one of the selected sources AND have
one of the selected types.


**Symbol Source Filters**- this group determines which symbols (based on
how they originated) should be included in the query.  At least one of the source
filters must be selected.


- **User Defined** - This filter includes all symbols named by the
user in the query.
- **Imported -** This filter includes all symbols named by some
imported information.
- **Analysis** - This filter includes all symbols created by
auto-analysis that do not have default names.
- **Default (Function)** - This filter includes all
function symbols that have default names.
- **Default (Labels)** - This filter includes all
non-function symbols that have default names (Ghidra generally creates default-named
symbols at any address that is referenced by some other location.)


**Symbol Type Filters -** This group of filters determines which types of
symbols to include in the query.  All symbols in Ghidra are one of the following types.
At least one of these type filters must be selected.


- **Instruction Labels -** labels at addresses with instructions.
Note these do NOT include labels where functions exist.
- **Data Labels -** labels at addresses with data or external labels.
Note these do NOT include labels where functions exists.
- **Functions -** labels at addresses where functions have been defined
(includes external functions).
- **Namespaces -** Namespace name symbols.
- **Classes -** C++ class names symbols.
- **External Library -** External library name symbols.
- **Parameters -** Function parameter name symbols.
- **Local Variables -** Function local variable name symbols.
- **Global Register Variable -** global register variable name
symbols.


Use the ***Select All*** button to select all symbol types and the
***Clear All*** to de-select all types.


<a name="advancedfilters"></a>**Advanced Symbol Filters -** Advanced
filters are used to further refine a query to only include symbols that meet various specific
criteria. Each of the advanced filters only applies to a subset of the symbol types, so
to use one of these filters, the appropriate symbol type filter must also be selected.
Advanced filters that do not have any of their associated type filters set, are
disabled. Advanced filters can be tricky to use because each filter only applies to a
subset of the types and has no effect on the other selected types during the
query.  See the [examples](#sample-queries) below for more information.


- **Externals -** Accepts only those symbols which are external.
- **Non-Externals -** Accepts only those symbols which are not
external.
- **Primary Labels -** Accepts only labels that are the primary label at
an address.  Applies to *Labels and Functions.*
- **Non-Primary Labels -** Accepts only labels that are not the primary
label at an address. Applies to *Labels and Functions.*
- **Globals -** Accepts the symbol if it is in the global
namespace.  Applies to *Labels, Functions, Namespaces,* and *classes.*
- **Locals -** Accepts the symbol if it is NOT in the global
namespace.  Applies to *Labels, Functions, Namespaces,* and *classes.*
- **Register Variables -** Accepts function parameters or local
variables that are register based. Applies to *Parameters* and *local
variables.*
- **Stack Variables -** Accepts function parameters or local variables
that are stack based. Applies to *Parameters* and *local variables.*
- **Entry Points -** Accepts labels or functions at external entry
points. Applies to *Labels* and *Functions.*
- **Subroutines -** Accepts labels that are "called" by some
instruction. (Does not include labels where functions are defined.) Applies to
*Labels.*
- **Not In Memory -** Accepts labels that are at an address not
contained in memory. Applies to *Labels.*
- **Unreferenced -** Accepts labels or functions that have no
references to them (also known as "dead code"). Applies to *Labels* and
*functions.*
- **Offcut Labels -** Accepts labels that are at an address that is not
the start of an instruction or data. Applies to *Labels.*


*Advanced Filters* affect the query using the following algorithm.
For each symbol that matches the selected source(s) and symbol type(s):


1. Find all selected advanced filters that are appropriate for the
symbol's type.
2. If no selected advanced filters are appropriate, include the
symbol.
3. If at least one advanced filter is appropriate, then the symbol is
included if at least one of those filters accepts the symbol.


Select the *Use Advanced Filters* checkbox to see the advanced
filters.


![](images/Filter2.png)


The ***Reset Filters*** button sets all checkboxes back to their
default states.


### **Sample Queries**


#### Example 1:


Setup - the following checkboxes are selected:


- Symbol Source:  User Defined
- Symbol Types:  Instruction Labels, Data Labels,  and
Function Labels
- Advanced Filter: none


Result:


- All labels and functions that are "user defined" will be shown in the
symbol table.


#### Example 2:


Setup:


- Symbol Source: User Defined, Imported, Analysis, and Default
- Symbol Types: Instruction Labels and Data Labels
- Advanced Filter: Subroutines


Result:


- All labels that are the start of a subroutine (not including
functions) are displayed.


If you want to see all subroutines including those that have been
defined as functions, also select the Functions type filter.


#### Example 3:


Setup:


- Symbol Source: User Defined, Imported, Analysis, and Default
- Symbol Types: Functions Labels and Parameters
- Advanced Filter: Stack Variables.


Result:


- All functions are displayed
- All parameters that are stack based are displayed. (Register
parameters have been filtered out.)


Note that the advanced filter *Stack Variables* is applicable only
to Parameters, and  therefore did not affect the display of functions.


#### Example 4:


Setup:


- Symbol Source: User Defined, Imported, Analysis, and Default
- Symbol Types: Instruction Labels, Data Labels, and Function
Labels
- Advanced Filter: Primary Labels and Non-primary Labels.


Result:


- All labels are displayed


Note that since all labels are either Primary labels or Non-primary
Labels, selecting both of these advanced filters accomplished nothing.  The results
would have been the same if neither was selected.


*Provided by: *Symbol Table Plugin**


**Related Topics:**


- [Labels](../LabelMgrPlugin/Labels.md)
- [Listing
Display Options](../CodeBrowserPlugin/CodeBrowserOptions.md#color-and-fonts)


---

[← Previous: PyGhidra Interpreter](../PyGhidra/interpreter.md) | [Next: Symbol References →](symbol_references.md)
