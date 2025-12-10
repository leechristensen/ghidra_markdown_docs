[Home](../index.md) > [BookmarkPlugin](index.md) > Bookmarks

# Bookmarks


Bookmarks are used to flag addresses of interest in a Program. Each Bookmark consists of an
address, a type, a name, a category (optional), and a description (optional). Bookmarks may be
organized using the category field. Ghidra places various Bookmark icons in the [Marker Margin](../CodeBrowserPlugin/CodeBrowser.md#margin-marker) of the [Code Browser](../CodeBrowserPlugin/CodeBrowser.md) to indicate locations of
defined bookmarks. The tooltip (shown when the mouse hovers over the Bookmark icon in the
Marker Margin) shows the Bookmark's type and comment.


The type refers to how the bookmark was added. Ghidra supplies five types of bookmarks:


| Bookmark Types |  |  |
| --- | --- | --- |
| Type (icon) | How Bookmark is Added | Navigator Color |
| --- | --- | --- |
| Note ![notes.gif](../icons/notes.gif) | Added via the [Note Bookmarkdialog](#add-a-bookmark-in-the-codebrowser) ; *Notes* are intended to be user-defined only. | Purple |
| Info ![information.png](../icons/information.png) | May be added by a plugin to mark an address of interest. | Cyan |
| Analysis ![applications-system.png](../icons/applications-system.png) | Added during the [Auto Analysis](../AutoAnalysisPlugin/AutoAnalysis.md) process.               Indicates automatic changes which have been made to the program (e.g., code found,               address tables, etc.). | Orange |
| Error ![edit-delete.png](../icons/edit-delete.png) | Added by the [disassembler](../DisassemblerPlugin/Disassembly.md) or [Auto Analysis](../AutoAnalysisPlugin/AutoAnalysis.md) process when an               unexpected condition is identified at a specific address (e.g., bad               instruction). | Red |
| *Unknown* ![unknown.gif](../icons/unknown.gif)   | Represents a custom Bookmark type which was added by a plugin not               currently configured into the tool. A properly designed plugin will assign a custom               icon and color to its custom type.   | Magenta   |


Ghidra also places a marker for the bookmark in the [Navigation Margin](../CodeBrowserPlugin/CodeBrowser.md#navigation-marker) of the
Code Browser. Clicking on the Navigation Margin causes the Code Browser to go to that address,
and centers it in the browser.


The following paragraphs describes the [*Bookmarks
window*](#bookmarks-window), and how to [add](#add-a-bookmark-in-the-codebrowser) and [remove](#remove-bookmarks) bookmarks.


## **Add a Bookmark (in the CodeBrowser)**


![](images/AddBookmarkDialog.png)


To add a Note Bookmark,


1. Position the cursor at an address
2. **Right-mouse-click** in the Code Browser, select **Bookmark**
3. The *Address* field on the *Note Bookmark* dialog shows the location where
the bookmark will be added
4. Enter a *Category* (optional) or choose an existing one from the combo box
5. Enter a *Description* (optional); if an end of line comment exists at this
address, then this text becomes the default description of the bookmark, as shown in the
image above.
6. Click on the **OK** button.


> **Tip:** When adding a bookmark with multiple selections in the
Code Browser, the Bookmark Top of Each Selection checkbox is both enabled and selected by default.
Leave the checkbox selected to create a bookmark at the start of each address range in the
selection. Deselecting the checkbox will cause the bookmark to be created at the cursor
location.


| ![before](images/Before.png)   Before Adding Bookmarks to Selection   | ![after](images/After.png)   After Adding Bookmarks to Selection   |
| --- | --- |


The following image depicts the Code Browser with Bookmarks. Notice the checkmarks in the
[Marker Margin](../CodeBrowserPlugin/CodeBrowser.md#margin-marker) on
the left and the markers in the [Navigation Margin](../CodeBrowserPlugin/CodeBrowser.md#navigation-marker) on
the right.


![](images/MarkerForBookmark.png)


## **Remove a Bookmark (in the CodeBrowser)**


To remove a bookmark,


1. Position the cursor on the address of the bookmark to be deleted
2. From the [Marker
Margin](../CodeBrowserPlugin/CodeBrowser.md#margin-marker), right-mouse-click, select **Delete Bookmark →  `<type>`: `<description>`**


## **Bookmarks Window**


The *Bookmarks* window lists all of the bookmarks within a Program, including the
bookmark type, category, description, address, label, and code unit where the bookmark was
placed. Click on a Bookmark to navigate to the selected address in the [Code Browser](../CodeBrowserPlugin/CodeBrowser.md).


![](images/Bookmarks.png)


To display the *Bookmarks* window, click the bookmark icon ![notes.gif](../icons/notes.gif) in the Code Browser toolbar, or select the **Window →  Bookmarks** option from the menu.


Each of the columns may be sorted by clicking on the header. The sort graphic illustrates
which column is being sorted on, and whether it is ascending (![Sort Ascending](../icons/sortascending.png) ) or descending (![Sort Descending](../icons/sortdescending.png) ). In the image above, the *Preview* column is
sorted in ascending alphabetical order. By default, the bookmarks are sorted in ascending
order by the *Type* column.


In the Bookmark table, only the *Category* and *Description* columns are editable. To edit entries in these columns,
double-click on the appropriate cell and begin typing. Click outside of the cell to apply the
changes. When the *Category* column is being edited, it shows a combo box, listing all
of the categories. Choose an existing category or enter a new one. If a new category in
entered, the combo box is updated.


![](images/BookmarksFilter.png)


The list of Bookmarks displayed can be filtered by clicking
the Filter button ![view-filter.png](../icons/view-filter.png) in the toolbar of the Bookmark
Window. The displayed bookmarks will correspond to the selected checkboxes in the *Bookmark
Filter* dialog.


> **Note:** You may also filter the contents of the
bookmark table by using the filter text field .


The following describes the features available from the Bookmarks window (Note: some of
these features are also available from inside the CodeBrowser):


### Edit Category


1. Double click in a *Category* cell to display the cell editor.
2. Click on the down-arrow button in the cell editor to display the list of
categories.
3. Select a category from the list OR enter a new category in the cell editor.
4. Press the **`<Enter>`** key or click outside of the editor.


### Edit Description


1. Double click on a *Description* cell to display the cell editor.
2. Enter a new description.
3. Press the **`<Enter>`** key or click outside of the editor.


### Change the Sort Order


Click on the desired column header to change the sort order.



### **Navigate to a Bookmark**


Click anywhere in the row to navigate to the bookmark.



### Filter Bookmarks


1. Click the Filter ![Configure Filter](../icons/exec.png) button in the local
toolbar of the *Bookmark*s window to display the *Bookmark Filter* dialog.
2. Configure filter information.
3. Click on the **OK** button.


> **Tip:** If you have turned off some of the filter types, then the filter icon will show
a checkmark ( ).


> **Note:** You may save the settings of the bookmark
filter dialog by saving the tool.


In addition to filtering on the type of bookmarks you
may also filter the contents of the bookmark table by entering text into the filter text
field found at the bottom of the bookmark table. This filter will include only those
Bookmarks whose Category or Description contain the specified text. For example, to show
only the entry point bookmarks, you would enter "entry" in the filter field. The results
would show only those bookmarks with a Category or Description containing the word "entry".
The text filter is not case sensitive, nor does it support *[Regular Expressions](../Glossary/glossary.md#regular-expression)*.


### **Reorder Columns**


Reorder columns in the Bookmarks window by dragging the column header to another position
in the table.



### Make Selection in the Code Browser


1. Select one or more rows in the Bookmarks table.
2. Click the Select Bookmark Locations ![Make Selection](../icons/stack.png)
button in the local toolbar.
3. The corresponding addresses are selected in the browser.
4. Navigate to the selected addressed by using the [navigation buttons](../Selection/Selecting.md#navigating-over-a-selection) (![NextSelectionBlock16.gif](../icons/NextSelectionBlock16.gif) , ![PreviousSelectionBlock16.gif](../icons/PreviousSelectionBlock16.gif) ) on the *main* tool bar.


### Remove Bookmarks


1. Select one or more rows in the Bookmarks table.
2. Hit the **`<Delete>`** key, or press the ![edit-delete.png](../icons/edit-delete.png) icon on the *Bookmarks* toolbar, or right mouse click and
choose the **Delete** option.


### Dismiss the *Bookmarks* Window


Click the **Dismiss** button to exit the *Bookmarks* window.



*Provided by: *Bookmarks* Plugin*


**Related Topics:**


- [Navigate on Selection](../Selection/Selecting.md)
- [Marker
Margin](../CodeBrowserPlugin/CodeBrowser.md#margin-marker)
- [Code Browser](../CodeBrowserPlugin/CodeBrowser.md)


---

[← Previous: Set Register Values](../RegisterPlugin/Registers.md) | [Next: Clear →](../ClearPlugin/Clear.md)
