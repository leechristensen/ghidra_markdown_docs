[Home](../index.md) > [Search](index.md) > Memory

# Search Memory


The memory search feature locates sequences of bytes in program memory. The search is
based on user entered values which can be specified in a variety of formats such as hex,
binary, string, and decimal values. The hex and binary formats support "wildcards" which can
match any bit or nibbles depending on the format. String search also supports the use of [regular expression](Search_Formats.md#regularexpressions) searches.


To create a new memory search window, select **Search**  → **Memory** from the main tool menu or use the default keybinding
"S".


> **Tip:** By default, search windows and their
tabs display "Search Memory:" followed by the search string and the program name. This
can be changed by right-clicking on the title or table to change its name. (This is true
for all transient windows.)


## Contents


- [Memory Search Window](#memory-search-window)
- [Search Controls](#search-controls)
- [Scan Controls](#scan-controls)
- [Results Table](#results-table)
- [Options](#options)
- [Search Formats](#search-formats)
- [Actions](#actions)
- [Combining Searches](#combining-searches)
- [Repeating Last Search Forwards/Backwards](#repeating-searches)
- [Highlight Search Options](#highlight-options)


## Memory Search Window


The Memory Search Window provides controls and options for entering search values and
and a table for displaying the search results. It supports both bulk searching and
incremental searching forwards and backwards. Also, users can perform additional searches
and combine those results with the existing results using set operations. The window also
has a "scan" feature which will re-examine the bytes of the current results set, looking
for memory changes at those locations (this is most useful when debugging). Scanning has an
option for reducing the results to those that either changed, didn't change, were
incremented, or were decremented.


![](images/MemorySearchProvider.png)


*Memory Search Window*


### Search Controls


At the top of the window as shown above, there are several GUI elements for initializing and
executing a memory byte search. These controls can be closed from the view after a search
to give more space to view results using the ![Search](../icons/view_top_bottom.png) toolbar button.


#### Search Format Field:


This is a drop-down list of formats whose selected format determines how to
interpret the text in the *Search Input Field*. The format will convert the user's
input into a sequence of bytes (and possibly masks). Details on each format are
described in the [*Search Formats*](Search_Formats.md) section.


#### Search Input Field:


Next to the *Search Format* drop-down, there is a text field where users can
enter one or more values to be searched. This field performs validation depending on
the active format. For example, when the format is *Hex*, users can only enter
hexadecimal values.


#### Previous Search Drop Down:


At the end of the input field, there is a drop-down list of previous searches.
Selecting one of these will populate the input field with that previous search input,
as well as the relevant settings that were used in that search such as the search
format.


#### Search Button:


Pressing the search button will initiate a search. When the results table is empty,
the only choice is to do an initial search. If there are current results showing in the
table, a drop-down will appear at the back of the button, allowing the user to combine
new search results with the existing results using set operations. See the
[*Combining Searches*](#combining-searches) section
below for more details.


#### Byte Sequence Field:


This field is used to show the user the bytes sequence that will be search for based
on the format and the user input entered. Hovering on this field will also display the
masks that will be used (if applicable).


#### Selection Only Checkbox:


If there is a current selection, then this checkbox will be enabled and provide the
user with the option to restrict the search to only the selected addresses. Note that
there is an action that controls whether this option will be selected automatically if
a selection exists.


### Scan Controls


The scan controls are used to re-examine search results, looking for values that have
changed since the search was initiated. This is primary useful when debugging. The
scan controls are not showing by default. Pressing the ![Scan](../icons/view_bottom.png) toolbar button will show the scan panel just
above the results table.


![](images/MemorySearchProviderWithScanPanelOn.png)


*Memory Search Window With Scan Controls Showing*


#### Scan Values Button:


This button initiates a scan of the byte values in all the matches in the results
table. Depending on the selected scan option, the set of matches in the table may be
reduced based on the values that changed.


#### Scan Option Radio Buttons


One of the following buttons can be selected and they determine how the set of
current matches should be reduced based on changed values.


- **Equals** This option will keep all matches whose values haven't changed and
remove any matches whose bytes have changed.
- **Not Equals** This option will keep all matches whose values have changed and
will remove any matches whose bytes have not changed.
- **Increased** This option will keep all matches whose values have increased
and will remove any matches whose values decreased or stayed the same.
- **Decreased** This option will keep all matches whose values have decreased
and will remove any matches whose values increased or stayed the same.


> **Tip:** The Increased or Decreased options really only make sense for matches that represent numerical
values such as integers or floats. In other cases it makes the determination based on
the first byte in the sequence that changed, as if they were a sequence of 1 byte
unsigned values.


> **Tip:** Another way to see changed bytes is
to use the Refresh toolbar action. This will
update the bytes for each search result and show them in red without reducing the set
of results.


### Results Table


The bottom part of the window is the search results table. Each row in the table
represents one search match. The table can contain combined results from multiple
searches. At the bottom of the results table, all the standard table filters are
available. The table has the following default columns, but additional columns can be
added by right-clicking on any column header.


- **Location:** Displays the address of the first byte in the matching
sequence.
- **Match Bytes:** Displays the bytes of the matching sequence. (Note: if you
refresh or scan, the bytes can change. Changed bytes will be displayed in red.)
- **Match Value:** Displays the matching bytes as a value where the value is
determined by the *Search Format*. Note that not all formats have a meaningful
value, in which case the column value will be empty.
- **Label:** Displays any labels that are present at the match address.
- **Code Unit:** Displays the instruction or data that the match address.


### Options


The options panel is not displayed by default. Pressing the ![Options](../icons/view_left_right.png) toolbar button will show them along the right side of the
window.


![](images/MemorySearchProviderWithOptionsOn.png)


*Memory Search Window With Options Open*


#### Byte Options


These are general options that affect most searches.


- **Endianess:** This chooses the byte ordering for values that are larger than
one byte. Big Endian orders the bytes most significant first. Little Endian orders the
bytes least significant first.
**Alignment:** The alignment requires that matches must start on an address that
has an offset that is a multiple of the specified integer field. For example, an
alignment of two would require that the address have an even value.


#### Decimal Options


These options apply when parsing input as decimal values.


- **Size:** The size (in bytes) of the decimal values.
- **Unsigned:** If checked, the values will be interpreted as unsigned values
and the input field won't accept negative values.


#### String Options


These options apply when parsing input as string data.


- **Encoding:** Specified the char set used to convert between strings and
bytes. (ASCII, UTF8, or UTF 16)
- **Case Sensitive:** If unselected, causes mask bytes to be generated such that
the search will not be case sensitive. Otherwise, the bytes must match exactly the
input the user entered.
- **Escape Sequences:** Determines if standard escape sequences are interpreted
literally or not. For example, if checked, and the user enters "\n", the search will
look for an end of line character. If unchecked, the search will look for a "\"
followed by an "n". Supported escape sequences include "\n", "\r", "\b", "\f", "\0",
"\x##", "\u####", "\U#########".


#### Code Type Filters


These are filters that can be applied to choose what type(s) of code units to
include in the results. By default, they are all selected. The types are:


- **Instructions:** Include matches that start at or in an instruction.
- **Defined Data:** Include matches that start at or in a define data.
- **Undefined Data:** Include matches that start at or in undefined data.


#### Memory Regions


Choose one or more memory regions to search. The available regions can vary depending
on the context, but the default regions are:


- **Loaded Blocks:** These include all the memory blocks defined that are actually
part of a loaded executable binary. On by default.
- **Other Blocks:** These are other than loaded blocks, typically representing
file header data. Off by default.


## Search Formats


The selected format determines how the user input is used to generate a search byte
sequence (and possibly mask byte sequence). They are also used to format bytes back into
"values" to be displayed in the table, if applicable.


See the page on [Search Formats](Search_Formats.md) for full details on each
format.


## Actions


### Incremental Search Forward


This action searches forward in memory, starting at the address just after the current
cursor location. It will continue until a match is found or the highest address in the
search space is reached. It does not "wrap". If a match is found, it is added to the
current table of results.


### Incremental Search Backwards


This action searches backwards in memory, starting at the address just before the
current cursor location. It will continue until a match is found or the lowest address in
the search space is reached. It does not "wrap". If a match is found, it is added to
the current table of results.


### Refresh


This action will read the bytes again from memory for every match in the results
table, looking to see if any of the bytes have changed. If so, the *Match Bytes* and
*Match Value* columns will display the changed values in red.


### Toggle
Search Controls


This action toggles the [search controls](#search-controls) on or off.


### Toggle Scan
Controls


This action toggles the [scan controls](#scan-controls) on or off.


### Toggle
Options Panel


This action toggles the [options display](#options) on or off.


### Make Selection


This action will create a selection in the associated view from all the currently
selected match table rows.


### Toggle Single Click
Navigation


This action toggles on or off whether a single row selection change triggers
navigation in the associated view. If this option is off, the user must double-click on a
row to navigate in the associated view.


### Delete Selected
Table Rows


This action deletes all selected rows in the results match table.


## Combining Searches


Results from multiple searches can be combined in various ways. These options are only
available once you have results in the table. Once results are present, the *Search
Button* changes to a button that has a drop down menu that allows you do decide how you
want additional searches to interact with the current results showing in the results table.
The options are as follows:


#### New Search


This option causes all existing result matches to be replaced with the results of the new
search. When this option is selected, the button text will show "New Search".


> **Tip:** This does not create a new
search memory window, but re-uses this window.  To create a new
search window, you must go back to the search memory action from the main menu.


#### A union B


This option adds the results from the new search to all the existing result matches. When
this option is selected, the button text will show "Add To Search".



#### A intersect B


This option will combine the results of the new search with the existing search, but only
keep results that are in both the existing result set and the new search result set. When
this option is selected, the button text will show "Intersect Search".



#### A xor B


This option will combine the results of the new search with the existing search, but only
keep results that are in either the new or existing results, but not both.
When this option is selected, the button text will show "Xor Search".



#### A - B


Subtracts the new results from the existing results. When
this option is selected, the button text will show "A-B Search".



#### B - A


Subtracts the existing results from the new results. When this option is
selected, the button text will show "B-A Search".



> **Tip:** Many of these set operations only make
sense if you do advanced searches using wildcards. For example, if you do a search for
integer values of 5, it would make no sense to intersect that with a search for integer
values of 3. The sets are mutually exclusive, so the intersection would be empty.
Explaining how to take advantage of these options is beyond the scope of this document.


## Search Forward/Backwards Using Global Actions


Once at least one search has been executed using the [*Memory Search Window*](#memory-search-window), the search can be repeated in an
incremental fashion outside a search window using global actions in the main tool menu or
their assigned default keybindings.


### Search Memory Forwards:


This action will use the input data and settings from the last memory search and begin
searching forwards in memory starting at the cursor location in the associated Listing
display. If a match is found, the cursor in the Listing will be placed on the found match
location. To execute this action, select **Search**  → **Search Memory Forwards** from the main tool menu or press
**F3** (the default keybinding.)


### Search Memory Backwards:


This action will use the input data and settings from the last memory search and begin
searching backwards in memory starting at the cursor location in the associated Listing
display. If a match is found, the cursor in the Listing will be placed on the found match
location. To execute this action, select **Search**  → **Search Memory Backwards** from the main tool menu or press
**`<Shift>`F3** (the default keybinding.)


## Highlight Search Options


You can control how the bytes found in the search be highlighted in the Code Browser by
selecting the *Highlight Search Results* checkbox on the Search Options panel. To view
the Search Options, select **Edit** →
**Tool Options...** from the tool menu, then select the *Search* node in the
Options tree in the Options dialog. You can also change the highlight color. Click on the
color bar next to *Highlight Color* to bring up a color chooser. Choose the new color,
click on the **OK** button. Apply your changes by clicking on the **OK** or
**Apply** button on the Options dialog.


> **Note:** Highlights are displayed for the
last search that you did. For example, if you bring up the Search Program Text dialog and
search for text, that string now becomes the new highlight string. Similarly, if you
invoke cursor
text highlighting , that becomes the new highlight string.


Highlights are removed when you close the search window.


*Provided by: *Memory Search Plugin**


**Related Topics:**


- [Searching Program Text](Searching.md)
- [Regular Expressions](Regular_Expressions.md)


---

[← Previous: Decompiled Text](../DecompilerTextFinderPlugin/Decompiler_Text_Finder.md) | [Next: Text →](Search_Program_Text.md)
