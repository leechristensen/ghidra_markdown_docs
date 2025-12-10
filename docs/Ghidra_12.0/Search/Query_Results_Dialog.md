[Home](../index.md) > [Search](index.md) > Query Results Window

# Search Results Window


The *Search Results* window displays search results from various sources (plugins). The
window is useful for navigating to a resultant location or selecting some number of result
locations for another operation that requires a selection. The information displayed in each
column may differ depending on the search operation that populated the window. However, the
window's capabilities are the same. The image below shows the results of a search. You will
also see the *Search Results* window when you do a [Go To](../Navigation/Navigation.md#go-to-address-label-or-expression) for matching a wildcard
entry.


| ![](images/QueryResultsSearch.png) |
| --- |


Each row of the table is associated with an address or location within the program. There
may be multiple entries for the same address, depending on the type of search. For example,
when searching text, a string may appear multiple times in the same pre-comment. So, you will
see an entry for each in the Search Results window. The title bar shows the number of entries
being displayed.


The tool has an option for the maximum number of search results. The search will stop after
this number has been exceeded. To see more search results,
[increase your search
limit](Search_Program_Text.md#search-limit-option).


### Navigation


As with most tables in Ghidra, you may change the location of the cursor within the tool
by clicking on the various table cells. The location to which the cursor is moved depends
upon which table cell is clicked. For example, clicking on the location column will move the
cursor to the location where the match was found. Alternatively, clicking on a label in the
label column will move the cursor to the corresponding label in the listing panel.


### Marker Margins


When searching strings or memory, a yellow arrow marker ![searchm_obj.gif](../icons/searchm_obj.gif) is placed in the left hand marker margin at
each location in the browser that a match was found. The location of each search result in the
entire view is displayed as a yellow box in the right hand Navigation Margin. You can
navigate to a search result by left-mouse-clicking on the yellow box in the Navigation margin.
The Navigation margin provides a general overview of where in the program any search results
were found.


### Renaming Windows


*see [Docking Windows - Renaming Windows](../DockingWindows/Docking_Windows.md#renaming-components)*


## Actions


### Make Selection ![Make Selection](../icons/stack.png)


A selection in the Listing can be created from the entries in the results table.
The selection can also be used as input to another operation that uses
the current selection, e.g., a follow-on search that is restricted to the results of the
first search using the current selection.


To create a selection from all the result items,


1. Click in the results table and press `Ctrl+A`.
2. Click on the ![Make Selection](../icons/stack.png) in
the tool bar, or right mouse click and choose **Make Selection**.
3. The current selection will be set to the address of each result item.


To create a selection from a subset of the items,


1. Select the result items with the `Ctrl+left-mouse` or
`Shift+left-mouse`.
2. Press and hold the right mouse button over the results table.
3. Click on the ![Make Selection](../icons/stack.png) in
the tool bar, or right mouse click and choose **Make Selection**.
4. The current selection will be set to the address of all the highlighted items.


### Remove Items ![table_delete.png](../icons/table_delete.png)


You can remove entries from the table via this action.  Items are **only** removed
from the table--no program data is changed.  This can be useful when you wish to
exclude results that are of no interest to you.


### Selection Navigation ![locationIn.gif](../icons/locationIn.gif)


This action causes the Listing to navigate to the address represented by a row when
that row is selected. Toggling this action on allows you to use the up and down arrow keys to
change the selection in the table while also navigating to that address in the Listing.
You may also use this action to trigger navigation when single-clicking a table row.


**Related Topics:**


- [Tool
Options](../Tool/ToolOptions_Dialog.md)
- [Text Search](Search_Program_Text.md)
- [Go To](../Navigation/Navigation.md#go-to-address-label-or-expression)


---

[← Previous: Direct References](Search_for_DirectReferences.md) | [Next: Search for Code and Functions →](../RandomForestFunctionFinderPlugin/RandomForestFunctionFinderPlugin.md)
