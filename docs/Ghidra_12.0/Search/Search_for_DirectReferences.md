[Home](../index.md) > [Search](index.md) > Direct References

# Search for Direct References


Search for Direct References will search the entire program for possible direct references
to the current location or to locations within the current selection in the program. This
search attempts to find the actual bytes that make up the address of the current
location/selection. The search takes into account the [endianness](../Glossary/glossary.md#endian) of the processor. The results are
displayed in a [Query Results](Query_Results_Dialog.md) table. The following table
shows the results of searching for direct references to a location (i.e. the program doesn't
have a selection). You can navigate to any resulting reference by selecting it in the
table.


| ![](images/DirectReferences.png)   |
| --- |


The Search Results Table shows the following for a search on a location:


- **From Location** - address of the possible direct reference
- **Label** - primary label at the location of the possible direct reference
- **From Preview** - current definition of the code unit at the location of the possible
direct reference
- **To Location** - address that is being referred to directly
- **To Preview** - current definition of the code unit at the "referred to"
location


To search for possible direct references to an address,


1. Click on the address in the [Code
Browser](../CodeBrowserPlugin/CodeBrowser.md).
2. Select **Search →  for Direct
References...**
3. If the search will take a while, an "in progress" dialog pops up so that you can see the
search progress, as well as cancel the search at any time.
4. A [Query Results](Query_Results_Dialog.md) window is displayed to show the
results of the search.


If you have a selection in your program when you perform the search,
***Search For Direct References*** will search for possible references to any of
the addresses in the selection. This can be very useful for finding
references into an area of memory that currently
has no references to it.


> **Tip:** To search for all possible
references within the current program's memory space,
press Ctrl+A to select the entire program
before performing the search


> **Note:** If you use this search multiple times on
different addresses without closing the window, one window will show all the results. Each
result for an address is displayed when you click on the tab at the bottom of the window.


> **Note:** This plugin works with 16-bit, 16-bit
segmented, and 32-bit programs.


### Restoring the Search Selection


If your search results came from searching on a selection, you can restore the program's
selection that was used for the search. To do this, click the ![menu16.gif](../icons/menu16.gif) menu button in the Search Results button bar and select
**Restore Search Results**. This will set the program selection back to what it was when
you initially performed the search.


### Filtering Results Based on Alignment


Once you have search results you can filter them based on the address alignment of the
**From Location**. To do this, click the ![menu16.gif](../icons/menu16.gif) menu
button in the Search Results button bar, pull right on **Alignment**, and select the
desired alignment (**1**, **2**, **4**, or **8**). This will limit the displayed
results to those where the **From Location** is an address that matches the selected byte
alignment.


## Actions


### Make Selection ![Make Selection](../icons/stack.png)


*See [Make Selection](Query_Results_Dialog.md#make-selection)*.


### Selection Navigation ![locationIn.gif](../icons/locationIn.gif)


*See [Selection Navigation](Query_Results_Dialog.md#selection-navigation)*.


*Provided by: *FindPossibleReferencesPlugin**


**Related Topics:**


- [Code
Browser](../CodeBrowserPlugin/CodeBrowser.md)
- [Query Results](Query_Results_Dialog.md)


---

[← Previous: Address Tables](Search_for_AddressTables.md) | [Next: Query Results Window →](Query_Results_Dialog.md)
