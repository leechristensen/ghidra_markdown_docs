[Home](../index.md) > [Search](index.md) > Search and Replace

<a name="search-and-replace"></a>


# Search And Replace


The search and replace feature allows to users to search for specific text sequences in
various Ghidra elements and replace that text sequence with a different text sequence. Using
this feature, many different elements in Ghidra can be renamed including labels, functions,
namespaces, parameters, datatypes, field elements, enum values, and others. This feature can
also be used to change comments placed on items such as instructions or data, structure field
element, or enum values.


By default, the search matches the text anywhere in an element ("contains"), but it has
full [regular expression](Search_Formats.md#examples-encoding-is-utf-16-case-sensitive-is-on-escape-sequences-is-off-big-endian) support where
users can easily perform a "starts with" or "ends with" search. Regular expression capture
groups are also supported which allows for complex replacing of disjoint strings. See the [examples](#navigation) section below for details.


To initiate a search and replace operation, select **Search**  → **Search and Replace** from the main tool menu.


## Search and Replace Dialog


The Search and Replace Dialog provides controls and options for performing and search
and replace operation.


![](images/SearchAndReplaceDialog.png)


*Search and Replace Dialog*


### Find


This is a text field for entering the text to be searched for in the selected Ghidra
elements. Elements are either the names of things such as labels, functions, datatypes,
or a comment associated with some item such as an instruction comment or structure field
comment.


Ghidra will find all the elements that contain the given text. To perform a "starts
with" or "ends with" search, you must enter a regular expression here and select the
regular expression option below.


There is also a drop down list of recent searches for this Ghidra session.


### Replace


This is a text field for entering the replacement text. This text will be used to
replace the text that matched the search text. For example, if a function was named
"startCat" and the goal was to change it to "startDog", you would enter "Cat" in the
Find field and "Dog" in this field.


This field also include a drop drow of the most recently enter replacement
strings.


### Options


#### Regular Expression


If selected, the search text will be interpreted as a regular expression. This
allows for complex search and replace operations. See the general section on [regular expressions](Search_Formats.md#examples-encoding-is-utf-16-case-sensitive-is-on-escape-sequences-is-off-big-endian) for more information. If
you want to anything other than a "contains" search, you must use a regular expression.
See below for examples on how to do this.


#### Case Sensitive


If selected, the entered search text must match exactly. Otherwise, the entered
search text can match regardless of the case of the search text or the target text.


#### Whole Word


If selected, the target text must be an entire word. In other words it must be
surrounded by white space or must be the first or last word in a word sequence. So,
when applied to renaming elements, the search text must match the entire name of the
element since element names cannot contain whitespace. But for comments, the search
text must entirely match one word withing the comment.


### Search For


This section contains a group of checkboxes used to turn on or off the type of Ghidra
elements to search. There are also buttons for selecting and deselecting all the element
checkboxes. At least one checkbox must be selected to perform a search.


- **Classes** - Search the names of classes.
- **Comments** - Search instruction or data comments. This includes pre-comments,
plate comments, end of line comments, post-comments, and repeatable comments.
- **Datatype Categories** - Search for the names of categories in the data types
tree.
- **Datatype Comments** - Search comments associated with datatypes. This includes
descriptions on enums and structures, datatype field comments, and enum value
comments.
- **Datatype Fields** - Search the names of structure or union field elements.
- **Datatypes** - Search the names of any nameable datatype (i.e., does
not search built-in datatypes such as byte, word, string, etc.)
- **Enum Values** - Search the names of enum values.
- **Functions** - Search the names of functions. (Note: This search does not
include external function names.)
- **Labels** - Search the names of labels. (Note: This search does not include
external labels.)
- **Local Variables** - Search the names of function local variables. (Note: This
does not include local variables derived by the decompiler that haven't been committed
to the database.)
- **Memory Blocks** - Search the names of Memory Blocks.
- **Namespaces** - Search the names of namespaces.
- **Parameters** - Search the names of function parameters.
- **Program Trees** - Search the names of modules and fragments defined in program
trees.


<a name="search-and-replace-results"></a>


## Results Window


After initiating a search and replace action, a results window will appear containing a
table showing each search match as an entry in the table. At this point, no changes have
been made to the program. This provides an opportunity to review the pending changes before
they are applied. The changes can now be applied all at once or individually.


![](images/SearchAndReplaceResults.png)


*Search and Replace Results Window*


### Table information


Each entry in the table represents one changes that can be applied.


#### Standard Columns


- **Original** - This column displays the original value of the matched
element.
- **Preview** - This column displays a preview of the value if this change is
applied.
- **Action** - The change to be applied. (either Rename for names or Update for
comments changes.)
- **Type** - This column displays the type of element being changed (label,
function, comment, etc.)
- **Status** - The icon displayed in this column indicates the status of this
change.


#### Status Icons


The status column will have one of the following icons to indicate item's
status:


- **Blank** - The change has not been applied.
- ![Warning](../icons/warning.png) - The change has some associated warning.
Hover on the status to get a detailed message of the issue.
- ![Error](../icons/emblem-important.png) - The change can't be applied. This status can
appear either before or after an attempt to apply has been made. Hover on the status
for more information.
- ![Done](../icons/tick.png) - The changes has been applied.


#### Optional Columns


- Current - Displays the current value of the element.
- Address - Displays the elements address if applicable, blank otherwise
- Path - Displays any path associated with the element, if applicable. The type of
path varies greatly with the element type.


#### Path Column Information


The Path column shows different path information depending on the element type:


- Classes - the namespace path.
- Datatype Categories - the parent category path.
- Datatype Comments - the parent category path.
- Datatype Names - the parent category path.
- Enum Values - the category path of the enum.
- Field Names - the category path of the structure or union.
- Functions - the namespace path.
- Labels - the namespace path.
- Local Variables - the namespace path.
- Namespaces - the parent namespace path.
- Parameters - the namespace path.
- Program Trees - the program tree module path


### Applying Changes


Changes can be applied in bulk or individually.


#### Apply All Button


Press this button to apply all items in the table, regardless of what is
selected.


<a name="apply-selected"></a>


#### Apply Selected Action


Press the ![Done](../icons/tick.png) toolbar button or use the
popup action **Execute Selected Action(s)** to apply just the selected entries in
the table. If only one item is selected when this is done, the selected item will
move to the next item in the table to facilitate a one at a time workflow.


<a name="auto-delete"></a>


> **Note:** There is also a popup toggle action
to turn on an option to auto delete applied entries from the table.


### Navigation


If the ![Navigate On Incoming Event](../icons/locationIn.gif) toolbar button is
selected, selecting items in the table will attempt to navigate to that item in the tool
if possible.


Double clicking (or pressing return key) will also attempt to navigate the tool to the
selected item. In addition, if the item is related to a datatype, an editor for that
datatype will be shown.


<a name="examples"></a>


## Search Examples


### Basic Searches


Without using regular expressions, you can find matches that contain the search text
or fully match the search text by turning on the "whole word" option. However, to
perform a "starts with" or "ends with" search, you must use a regular expression. Also,
you can do advanced match and replace using regular expressions capture groups.


The following examples assume we are trying to replace label names and we have the
following labels in our program:


- Apple
- myApple
- AppleJuice


| Search Type   | RegEx   | Whole Word   | Search For   | Replace With   | Matches   | Results   |
| --- | --- | --- | --- | --- | --- | --- |
| **Contains** | Off | Off | Apple | Pear | Apple, myApple, AppleJuice | Pear, myPear, PearJuice |
| **Matches Fully** | Off | On | Apple | Pear | Apple | Pear |
| **Starts With** | On | N/A | ^Apple | Pear | Apple, AppleJuice | Pear, PearJuice |
| **Ends With** | On | N/A | Apple$ | Pear | Apple, MyApple | Pear, MyPear |


### Advanced RegEx Searches


Regular Expression can do many advanced types of matching and replacing which is
beyond the scope of this document. However, a simple example using capture groups will
be given as follows:


| Search For   | Replace With   | Matches   | Results   |
| --- | --- | --- | --- |
| Red(.*)Blue(.*) | Green$1Purple$2 | RedApplesBlueBerries | GreenApplesPurpleBerries |


*Provided by: *SearchAndReplacePlugin**


**Related Topics:**


- [Searching](Searching.md)
- [Search Program Text](Search_Program_Text.md)


---

[← Previous: Text](Search_Program_Text.md) | [Next: Strings →](Search_for_Strings.md)
