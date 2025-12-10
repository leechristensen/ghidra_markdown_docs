[Home](../index.md) > [Navigation](index.md) > Go to Next/Previous

# Navigation


Often, users need to navigate to specific locations in a program.  Ghidra provides
several different ways to do this:


- Enter a particular address or label ([Go To](#go-to-address-label-or-expression))
- Double-click on any displayed label or address in the [Code Browser](../CodeBrowserPlugin/CodeBrowser.md#navigation) tool
- Jump directly to the [Next/Previous Code
Unit](#nextprevious-code-unit)
- Use the [Navigation History](#navigation-history) to return to
a previously visited location
- Specify a specific [Program Start
Location](#starting-program-location-options) when opening a program


## Go To Address, Label, or Expression


### To Perform a Go To:


1. In the menu-bar of a tool, select **Navigation  →  Go To...**
2. The *Go To* dialog will be displayed, as shown below:
3. Enter either an [address](#go-to-address), [label](#go-to-label),
[expression](#go-to-expression), or [file offset](#go-to-file-offset)
as specified below and press "OK"
4. If the address, label, expression, or file offset is valid, the Code Browser will be
repositioned to that location and the dialog will be dismissed
5. If the address, label, expression, or file offset is not valid, the dialog will display
an error message


| Go To Address, Label, Expression, or File Offset             Dialag |
| --- |


### Go To Address


Enter an address into the text area of the dialog. The value entered will be assumed to
be in hexadecimal. That is, "0x1000" and "1000" are the same value.


*When the program has multiple
address spaces and the destination address is ambiguous (based on the current location), a
query results dialog will be displayed.*


**Consider the following examples:**


Given:


A program with the following memory blocks **which reside in different address
spaces**:


| **Name** | **Start Address** | **End Address** |
| --- | --- | --- |
| BLOCK1 | BLOCK1:00000000 | BLOCK1:0000ffff |
| BLOCK2 | BLOCK2:00000000 | BLOCK2:0000ffff |
| BLOCK3 | BLOCK3:00000080 | BLOCK3:0000ffff |


Example #1 - Unambiguous address


1. Set the current location to BLOCK1:00001000
2. Goto address "5"
3. The destination is not ambiguous:
  - The BLOCK1 block has an address "5" so the listing will move to address 5.


Example #2 - Ambiguous Address


1. Set the current location to BLOCK3:00000080
2. Goto address "5"
3. The destination is ambiguous because:
  - The BLOCK3 block does not have an address "5"
  - Both the BLOCK1 and BLOCK2 blocks have an address "5"
4. A *[Query Results](../Search/Query_Results_Dialog.md)*
dialog will be displayed as shown in the image below.


| Ambiguous Destination Address |
| --- |


### Go To Label


Enter the name or namespace path of an existing label into the text field of the dialog.
The name and/or path may contain wildcards (* ? **).


#### Namespace Paths


A label name can be specified with or without namespace paths. Use the "::" delimiter
to separate namespace elements and the symbol name, with the symbol name always being the
last element.


Namespace paths do not have to be fully specified from the global namespace, so for
example, "a::b" will find the symbol "b" in a namespace "a", regardless of whether or not
the namespace "a" is global or in some other namespace. In other words, the namespace
path is relative to any namespace.


To require that the specified path be absolute (fully specified from the global
namespace), start the path with the "::" delimiter. So, for example, "::a::b" will only
match the symbol "b" if it is in a namespace "a" which is itself in the global
namespace.


#### Wildcards


Wildcard characters(* ** ?) can be used to match namespace names and/or symbol names.
If more than one match is found, the results are displayed in a **GoTo Query Results**
table


##### Supported Wildcards


| Wildcard   | Description   |
| --- | --- |
| * | Matches zero or more characters within a single namespace or                   symbol name. Does not match across :: delimiters. Also, it must match something                   at that level. So, "::*::*::a" only matches symbols that are exactly two                   namespace levels deep. |
| ? | Matches exactly one characters within a single namespace or symbol name. |
| ** | Matches 0 or more path elements. The '**' must not be mixed with other                   characters. The only valid forms are '::**::', '**::', or '::**'. See the examples                   below for use of this syntax. |


##### Wildcard Examples


| Input   | Descriptions   |
| --- | --- |
| abc* | Matches any symbol whose name starts with "abc" |
| abc*xyz | Matches any symbol whose name starts with "abc" and ends with "xyz" |
| abc?xyz | Matches any symbol whose name starts with "abc" and ends with "xyz" and has                 exactly 1 char between them |
| a::b | Matches any symbol named "b" whose immediate parent namespace is named "a" |
| ::a | Matches any global symbol named "a" |
| ::a::b | Matches any symbol named "b" whose immediate parent namespace is named "a" and                 "a" is in the global namespace |
| a::* | Matches any symbol whose immediate parent namespace is named "a" |
| a::*::z | Matches any symbol named "z" whose namespace two levels up is named "a" |
| *::*::z | Matches any symbol named "z" that is at least two levels below the global                 namespace |
| a::**::z | Matches any symbol named "z" that has a namespace named "a" anywhere in it's                 namespace ancestry |
| a::** | Matches any symbol that has a namespace named "a" anywhere in it's namespace                 ancestry |


##### Wildcard Examples (With sample full symbol paths of matching and not matching symbols)


| Input   | Matches   | Does Not Match   |
| --- | --- | --- |
| abc* | abc, abcdef | bcd, bc |
| abc*xyz | abcxyz, abc12xyz | abcz |
| abc?xyz | abcdxyz, abcexyz | abcxyz, abc12xyz |
| a::b | a::b, x::a::b, x::y::a::b | a::x::b |
| ::a | a | x::a, a::b |
| ::a::b | a::b | x::a::b |
| a::* | a::b, a::c, x::a::d | x::b, x::a |
| a::*::z | a::b::z, a::c::z, x::a::b::z | a::b::c::z |
| *::*::z | a::b::z, x::a::b::z | a::z |
| **::*::z | a::b::z, x::a::b::z, a::z | z |
| ::**::z | a::b::z, x::a::b::z, a::z | z |
| a::**::z | a::z, a::b::z, a::b::c::z | b::z, a::z::x |
| a::** | a::z, a::b::z, a::b::c::z, a::z::x | b::z, x::z |


#### Case Sensitive


By default, the values entered are case sensitive.  That is, "LAB1000" is not the
same as "lab1000."  If you want to find both of these labels, turn off the case
sensitive option.  If more than one match is found, they are displayed in a Query
Results dialog.


#### Dynamic Labels


This option determines if the query includes generic dynamically generated labels
(LAB*, DAT*, FUN*, etc.). If this option is off, only defined labels are searched.


> **Note:** Turning off this option can result
in significantly faster results in larger programs.


### Go To File Offset


Enter **file(n)**, where **n** is a file offset of the program's source file bytes
(at time of import), into the text area of the dialog. The file offset entered will be
assumed to be in decimal unless it is preceded by **0x**. That is, "file(0x1000)" and
"file(1000)" are different values.


*Ghidra does not support storing
source file bytes for all file formats. Searching for a file offset in these programs will
always yield no results.*


*When the program has multiple file
byte sources and the destination address is ambiguous, a query results dialog will be
displayed.*


### Go To Expression


Enter an arithmetic expression that can include addresses, symbols, or can be relative
to the current location. All numbers are assumed to be hexadecimal. Supported operators are
"+ - * / &lt;&lt; &gt;&gt;".  Also, parentheses are supported to control order of
expression evaluation.

For example:


| **ENTRY+10** | Positions the cursor at the address 0x10 addresses past the symbol ENTRY |
| --- | --- |
| **0x100000+30** | Positions the cursor at address 0x100030 |
| **0x100000+(2*10)** | Positions the cursor at address 0x100020 |
| **+20** | Positions the cursor at an address that is 0x20 past the current location |


### Repeating a Previous Go To


Each time a Go To Label or a Query is performed, it is stored in the drop-down box as
shown in the image below.


| Previous Go to List |
| --- |


To repeat a previous Go To or Query:


1. Select the item from the *Enter an address or label:* drop-down box
2. Click the **OK** button


### Error Messages


When a Go To or Query fails, an error message will be displayed in the status area of
the dialog.


1. Entering an invalid address or non-existing label
  - The dialog displays *"This is not a query, label, or address."*
2. Specifying a query that has no results
  - The dialog displays *"No results for ..."*, where "..." is the query
string.


*Provided by: *Go To Address or Label* plugin*


## Next/Previous Code Unit


The Next/Previous Code Unit feature allows the user to jump directly to the next or
previous Instruction, Data, Undefined, Function or Non Function. The search starts at the
current cursor location and proceeds either forward (next) or backwards (previous).


> **Note:** When searching for Instructions, Data
or Undefined items, Ghidra will skip all contiguous items of the same type. For example, if
the cursor is on an address with an Instruction, and you go to the next Instruction, then
all Instructions immediately following the current one will be skipped until a
non-Instruction is found. Once that non-instruction is found, then Ghidra will take you to
the next Instruction after the address of that non-Instruction.


### Search Direction


The ![down_arrow](../icons/down.png) icon indicates the search
will performed in the forward (next) direction, and the ![up_arrow](../icons/up.png) icon indicates the search will be performed in the backward
(previous) direction. To change the direction of the code unit search, toggle the arrow
icon on the toolbar.


Alternatively, holding the **SHIFT** key when clicking a navigation button will
temporarily invert the direction of the search.


### Invert Search Logic


The ![down_arrow](../icons/dialog-cancel.png) icon indicates the
search logic will be inverted / negated. The exact meaning of this depends upon the type of
search performed, as described below.


### Navigate to Instruction


To move the cursor to the next instruction click on the Navigate by Instruction icon,
![I](../icons/I.gif). This icon is disabled when no more
instructions exist in the current search direction.


If already on an instruction, **on the address field**, then this action will find the
next data or undefined data before finding the next instruction. This allows users to jump
between ranges of instructions.


![Note](../shared/note.yellow.png)When performing this
action while not on the address field, then the action will first go to the address
field for the current address if an instruction exists.  Subsequent invocations will
then work as described above.  This is convenient for jumping from a function
signature to the function entry point.


When inverted, this task, if on an instruction, will attempt to navigate to the next
data or undefined data. If not on an instruction, then this task will find the next
instruction and then find the data or undefined data after that.


### Navigate to Data


To move the cursor to the next data code unit, click on the Navigate by Data icon, ![D](../icons/D.gif). This icon is disabled when no more data code units
exist in the current search direction.


When inverted, this task, if on a data code unit, will attempt to navigate to the next
instruction or undefined data. If not on a data, then this task will find the next defined
data and then find the instruction or undefined data after that.


### Navigate to Undefined


To move the cursor to the next undefined code unit, click on the Navigate by Data icon,
![U](../icons/U.gif). This icon is disabled when no more undefined
code units exist in the current search direction.


When inverted, this task, if on an undefined code unit, will attempt to navigate to the
next instruction or data. If not on an undefined, then this task will find the next
undefined and then find the instruction or data after that.


### Navigate to Label


To move the cursor to the next Label, click on the Navigate by Label icon, ![L](../icons/L.gif).


When inverted, this task, if on an address with a label, will attempt to navigate to the
next code unit without a label. If not on an address with a label, then this task will find
the next label and then find the next code unit after that without a label.


### Navigate to Function


This (![F](../icons/F.gif)) action will move the cursor to the
next function in the current direction. If inside a function and the direction is towards
lower addresses, then this action will go to the current function's entry point.


When inverted, this task (![F](../icons/notF.gif)) will attempt to the
navigate to the next instruction block not contained in a function. This can be useful when
manually creating functions and stepping over them to identify potential function
candidates.


### Navigate to Matching Byte Values


This task (![V](../icons/V.png)) will attempt to navigate to the next
matching byte pattern of the code unit under the cursor.


When inverted, this task will attempt to the navigate to the first code-unit where the
byte value is different from the byte value of the first byte of the current code unit.
This can be useful when trying to navigate past a series of 0s or FFs


### Navigate to Bookmark


To move the cursor to the next bookmark, click on the Navigate by Bookmark icon, ![B](../icons/B.gif). You may use the pull-down menu to choose a specific
type of bookmark (![B](../icons/applications-system.png), ![B](../icons/edit-delete.png), ![B](../icons/information.png), ![B](../icons/notes.gif), ![B](../icons/warning.png), ![B](../icons/unknown.gif)) to navigate to as
opposed to all types.


When inverted, this task will attempt to navigate to then next address with a bookmark
different than what is selected in the pull-down menu of the icon. If the 'all bookmarks'
state is selected, then this task will simply navigate to the next address that has no
bookmark.


*Provided by: *Go To Next-Previous Code Unit* plugin*



This file is different than most, since it has multiple plugins contributing to the
content.  Add some space at the bottom of the file to separate this last contribution



## Next/Previous Function


Navigating to the next or previous function is a commonly used feature. As such, separate
actions have been created so that keybindings can be assigned for each direction.


### Next Function


This action navigates the cursor to the closest function entry point that is at an
address greater than the current address. The default keybinding is
`Control-Down Arrow`.


### Previous Function


This action navigates the cursor to the closest function entry point that is at an
address less than the current address. The default keybinding is
`Control-Up Arrow`.


*Provided by: *CodeBrowser* plugin*



This file is different than most, since it has multiple plugins contributing to the
content.  Add some space at the bottom of the file to separate this last contribution



## Navigation History


As the user performs various types of navigations, the current location is pushed onto the
navigation history stack.  The navigation history feature allows the user to revisit
previous locations.


### Go To Next/Previous Location


To traverse the history stack:


1. In the tool-bar, click either the **Go to previous location** (![left.png](../icons/left.png) ) button or the **Go to next location** (![right.png](../icons/right.png)) button
2. The Code Browser will be repositioned to the saved location


#### Some Operations that add to the navigation history:


- Go To Address or Label
- Double-clicking on operands containing addresses or labels
- Double-clicking on XREFs ([field](../CodeBrowserPlugin/Browser_Field_Formatter.md) in the [Code Browser](../CodeBrowserPlugin/CodeBrowser.md))
- Clicking on the start or end address of a memory block using the memory map
dialog
- Clicking on the address of an equate reference using the equates table
- Performing a search ([Memory](../Search/Search_Memory.md), [Program Text](../Search/Search_Program_Text.md), etc)


> **Note:** The button is only enabled after performing a


### Go To Next/Previous **Function** in History


These actions allow you to navigate to the next/previous functions in the history list,
skipping over any locations that are not in functions or are in the current function.


> **Note:** The behavior of the previous action
will vary slightly depending upon what component is focused. It is possible for a
non-Listing view to be showing a function that is not the current function in the
Listing. In this case, if the Listing has focus, then the previously visited function
will be the navigation destination. Alternatively, if a non-Listing widget (e.g., the
Decompiler) has focus and is showing a function, then that function being displayed will
be ignored when navigating to the previous function.


### Clear History


To clear the navigation history stack, select **Navigation  →  Clear History**


After clearing the history, the ![left.png](../icons/left.png) and
![right.png](../icons/right.png) buttons are disabled


*Provided by: *Next/Previous* plugin*



This file is different than most, since it has multiple plugins contributing to the
content.  Add some space at the bottom of the file to separate this contribution.



## Component Provider Navigation


This section lists actions that allow the user to navigate between component
providers.


### Go To Last Active Component


Allows the user to switch focus back to the previously focused component provider.


*Provided by: *ProviderNavigation* plugin*



This file is different than most, since it has multiple plugins contributing to the
content.  Add some space at the bottom of the file to separate this contribution.



---


## Navigation Options


**'Go To' in Current Program Only** - 'Go To' service will only search for and navigate
to locations in the current program. If this option is off and the search location is not
found in the current program, the 'Go To' action will search other open programs, possibly
resulting in the listing view switching to a different open program tab. By default, this
option is on, thereby guaranteeing that the listing view will not change to a different
program when performing a ['Go To' action](#go-to-address-label-or-expression).


**External Navigation** - Determines the behavior for navigation to external symbols
and references. By default, navigating to an external will attempt to navigate within the
current program to the first linkage reference (pointer or thunk). Alternatively, if an
external program has been associated with an import Library, then that program will be opened
and positioned to the selected external location if found.


**Follow Indirection** - Determines the behavior for navigation on indirect flow
references. By default, this option is disabled providing navigation to the referenced
pointer data. If enabled, the pointer will be followed to its referenced destination if
contained within the program's memory.


**Prefer Current Address Space** - Determines if the 'Go To' action prefers the current
address space when entering address offsets. For example, if your program has multiple
address spaces such as 'RAM' or 'DATA' and you enter 1000 into the 'Go To' field, you could
mean RAM:1000 or DATA:1000. If this option is on, then it will go to the address with the
address space that matches the current cursor location. Otherwise, it will show a list of
possible addresses for the given offset. The default is on for this option.


**Range Navigation** - Determines how [navigation of ranges](../Selection/Selecting.md#navigating-over-a-selection) (i.e.,
selection ranges and highlight ranges) takes place. By default, navigating to ranges will
place the cursor at the top of the next range. You may use this option to navigate to both
the top and the bottom of each range being navigated.


### Starting Program Location Options


The starting location for newly opened programs can be configured using the following
options:


**Start At** - Choose a starting program location option:


- Lowest Address - The program will open at the lowest address.
- Lowest Code Block Address - The program will open at the first executable memory
block. If no executable block found, it will go to lowest address.
- Preferred Symbol Name - The program will open at the first symbol name it finds that
matches a name in the "Start Symbols" option. If no symbol is found, it will try the
lowest code block, and finally the lowest address.
- Location When Last Closed - The program will open to the location it was at the last
time the program was closed. If this is the first time the program has been opened, it
will try to find a preferred symbol, then it will look for the lowest code block, and
finally lowest overall address


**<a name="start-symbols"></a>Start Symbols** - A comma separated list of symbol
names to be used as the starting location for the program if the "Preferred Symbol Name"
option is selected above. The first matching symbol found will be used as the starting
location for newly opened programs.


**Use Underscores** - If selected, each of the preferred symbols listed above will
also be searched for with either one or two underscores prepended to the name. For example,
if selected, it will search for "_main" and "__main" in addition to "main" when trying to
find a starting symbol.


### Initial Analysis Navigation Options


These options control the behavior of the tool after the initial analysis has
completed.


**Ask To Reposition Program** - If selected, the user will be prompted if they would
like the program to be positioned to any newly discovered starting symbols as specified in
the [Start Symbols](#starting-program-location-options) option.


**Auto Reposition If Not Moved** - If selected, the program will automatically be
reposition to any newly discovered starting symbols as specified in the [Start Symbols](#starting-program-location-options) option, provided the user has not manually moved the
cursor off the starting location address. If they have manually moved the cursor, then the
behavior will revert to the setting of the "Ask To Reposition Program" option above.



This file is different than most, since it has multiple plugins contributing to the
content.  Add some space at the bottom of the file to separate this contribution.



**Related Topics:**


- [Query Results](../Search/Query_Results_Dialog.md)
- [Code Browser](../CodeBrowserPlugin/CodeBrowser.md)
- [Search Memory](../Search/Search_Memory.md)
- [Search Program Text](../Search/Search_Program_Text.md)


---

[← Previous: Go to Address Label](Navigation.md) | [Next: Margin and Navigation Markers →](../CodeBrowserPlugin/CodeBrowser.md)
