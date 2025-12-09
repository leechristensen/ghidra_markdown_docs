# View Defined Strings


The View Defined Strings plugin will display all strings that have been explicitly defined
in the program. You can click on the address column and navigate to the string in the [Listing](../CodeBrowserPlugin/CodeBrowser.md).


![](images/Defined_String_Table.png)


This plugin is ***not*** intended to be used to locate undefined strings. Please see
[Search for Strings](../Search/Search_for_Strings.md) or
[Search for Encoded Strings](../Search/Search_for_Strings.md#encoded-strings-dialog) for this
feature.


## Defined Strings Table Columns


The Defined Strings table has several columns that display information about each
string instance.


- Location - address where string is found.  Double click in this column to navigate to the string.
- String Value - raw value of string.
- String Representation - formatted representation of the string (see
[String Settings](../DataPlugin/Data.md#stringsettings) for formatting settings)
or the translated value of the string.  Double click in this column to change the string's
representation into a value of your choice.  This is the
same as using the **Translate  →
Manual** menu item.
- Data Type - mnemonic or data type for the string type.
- Is Ascii - boolean flag that indicates the string has non-ASCII characters.
- Has Encoding Error - boolean flag that indicates the string had byte(s) that could not be converted by the character set.
This is usually caused by having the wrong character set or if the string isn't really a string.
- Charset - name of the character set that this string is encoded in.
- Unicode Script - a list of the scripts (alphabets) used in the string.


The **Is Ascii**, **Has Encoding Error**, **Unicode Script**, and **Charset** columns are not visible by default.  To display
them in the table, right click on the column header row and select
**Add/Remove Columns...**.


## Defined Strings Menus and Actions


### Make Selection


The Defined Strings window has an icon (![Make Selection](../icons/stack.png))
on the tool bar to make a selection in the Code Browser. To make a selection,


1. Select the rows containing the desired strings in the table.
2. Right mouse click and select the ![Make Selection](../icons/stack.png) **Make
Selection** option, OR select the ![Make Selection](../icons/stack.png)button on
the tool bar.


### Refresh


The strings shown in the Defined Strings window can be refreshed by:


- Right mouse click on any row and select the ![Refresh](../icons/reload3.png) **Refresh**
option, OR
- Select the ![Refresh](../icons/reload3.png)button on the tool bar.


> **Note:** The refresh icon on the toolbar will
appear grayed-out by default.  If potential changes to string data are detected,
the icon will become green in color.   The toolbar button can be pressed in either state
for a full table reload.


### Settings... and Default Settings...


Each data type in Ghidra allows different properties to be set on instances of that
data type.  The **Settings...** action in the right click popup menu allow changing
the settings for the highlighted rows.


Typical settings available for string data instances:


- Charset
- Render non-ASCII Unicode
- Translation


The **Default Settings...** action allows changing the settings for all instances
of a specific data type.


For more information, see [string settings](../DataPlugin/Data.md#stringsettings).


### Translate


Each string value can have a translated version of the value associated with it.  The
translated value will be displayed in **»chevrons«** in the **String
Representation** column.


For more information, see [Translate Strings Plugin](../TranslateStringsPlugin/TranslateStringsPlugin.md)
help.


*Provided by: *View Strings* Plugin*


**Related Topics:**


- [Search .. for
Strings](../Search/Search_for_Strings.md)
- [Operand Field
options](../CodeBrowserPlugin/CodeBrowserOptions.md#operands-field)
- [Listing](../CodeBrowserPlugin/CodeBrowser.md)
- [Translate
Strings Plugin](../TranslateStringsPlugin/TranslateStringsPlugin.md)
- [String data types](../DataPlugin/Data.md#stringdatatypes)
