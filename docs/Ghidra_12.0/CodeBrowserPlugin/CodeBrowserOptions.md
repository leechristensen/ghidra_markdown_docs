[Home](../index.md) > [CodeBrowserPlugin](index.md) > Configuration Options

# Listing Options


Attributes of the Listing can be customized using the [Tool Options Dialog](../Tool/ToolOptions_Dialog.md). These are the types of
attributes that can be customized:


- [Colors and Fonts](#popups)
- [Fields, Highlights, and Selections](#fields-highlights-selections)
- [Popups](#popups)


## Color and Fonts


To view or change colors and fonts for fields of the Listing, open the [Tool Options Dialog](../Tool/ToolOptions_Dialog.md) and select the *Listing
Display* node in the Options tree. The Listing Display panel will be displayed as shown
below.


| ![](images/CodeBrowserColors.png) |
| --- |


This panel is divided into the following sections:


### Font


Sets the default font, size and style for all text fields in the listing. The font and
size apply to all screen elements. The styles (bold/italic) will be used as the default for
each screen element unless individually customized using the [Style
Settings](#style-settings).


### Screen Element


The *Screen Element* lists all the customizable items that can be displayed by the
Listing. Some of the elements are fields such as the *Address* field. Others represent
the *type* of information in a field. For example, the operand field may contain a
label, scalar, address, or constant. Still others are *attributes* on the data in the
fields. An example of this is label field. A label can be primary or local. Screen elements
can be selected in order to change their associated color and font style.


The table below describes all the Screen Elements and indicates the fields in which they
appear.


| **Screen Element** | **Description** | **Field** |
| --- | --- | --- |
| Address | Addresses | Address field |
| Background* | N/A | N/A |
| Bad Reference Address | Addresses or labels that are not in                 memory | Operand field |
| Bytes | Bytes | Bytes field |
| Comment, Automatic | System-generated comments | EOL comment field |
| Comment, EOL | End-of-line comments | EOL comment field |
| Comment, Plate | Block comments | Plate comment field |
| Comment, Post | Below-line comments | Post comment field |
| Comment, Pre | Above-line comments | Pre comment field |
| Comment, Repeatable   | Repeatable comment at this code-unit that is displayed where there                 are references to this code unit   | EOL comment field   |
| Comment, Referenced Repeatable | Displays repeatable comment defined at                 code-unit referred to by this code unit | EOL comment field |
| Constant | Numbers | Operand field |
| Entry Point | Labels that are at Entry Points in a                 program | Label field |
| External Reference, Resolved | External addresses or labels | Operand field |
| Field Name | Name of elements in a structure or                 union | "Field Name" field |
| Flow Arrow, Active | Flow arrow when cursor **is** at the                 source | N/A |
| Flow Arrow, Not Active | Flow arrow when cursor is **not** at                 source | N/A |
| Function Name | Function name | Function Signature, Operands |
| Function Parameters | Parameter data types and names | Function Signature field |
| Function Return type | Data Type returned by the function | Function Signature field |
| Labels, Local | Labels that are local to a function | Label field |
| Labels, Non-primary | Additional labels at an address | Label field |
| Labels, Primary | Primary label at an address | Label field |
| Labels, Unreferenced | Labels at addresses that are not                 referenced | Label field |
| Mnemonic | Instruction or Data (Mnemonic) | Mnemonic field |
| Operands | defaults for items in operand field | Operand field |
| Registers | Registers | Operand field |
| Separator | Separator line (...) between address                 gaps | Separator field |
| Variable | Function variables | Variable Type, Variable Location, Variable                 Name, Variable Comment |
| Version Track | Version tracking information | Version tracker field |
| Xref | Cross reference addresses | Xref field |
| Xref, Offcut | Offcut cross reference addresses | Offcut references Xref field |


*The Background is a special case. Select this element to set the background color for
the Listing.


### Color


The color for the selected screen element is displayed in this section.


### Style Settings


By default, all screen elements use the style settings set in the [Font](#font) section. To customize individual screen elements, select the screen
element from the Screen Elements section and select the *custom* checkbox in the Style
Settings section. This will enable the *bold* and *italics* checkboxes which can
be used to customize the style of the selected screen element.


### Swatches/HSB/RGB


These tabbed components provide a variety of ways to choose a color for the selected
screen element.


#### Swatches


Click on the desired color-square to set the color of the currently selected screen
element.


#### HSB


This tab allows colors to be chosen using the hue, saturation, and brightness scale.
The radio button selects which scale will be controlled by the slider bar. Use the slider
bar to choose a value for the selected scale. This causes the large color box to display
all possible colors with that selected value. Click in the box to choose a color.


#### RGB


This tab allows colors to be chosen by entering a red, green, and blue value.


### Preview


The preview tab displays some sample code using the current set of screen element colors
and styles.


## Fields, Highlights, & Selections


There are other customizable options in addition to color and font. To view or change
these options, open the [Tool Options
Dialog](../Tool/ToolOptions_Dialog.md) and then open the *Listing Fields* node in the Options tree. Next, select the
appropriate field within the *Listing Fields* node to view or change the options for
that field. The available *Listing Field* options are:


### Address Field


**Show Block Name -**This option prepends the memory block name to the address in the
address field. For example, 0x10008000 might become .text:0x10008000.


**Fully Pad With Leading Zeros -** This option causes all addresses to be displayed
with leading zeros to make the address string length the same as the length of the largest
address in that address space.  For example, in a 32 bit address space program the
address 0x100 will be displayed as 00000100.


**Minimum Number of Address Digits -**This option is used to specify the minimum
number of digits that should be used to display the address.  The address string will
be displayed with leading zeros to make the length contain at least this number of
digits.  If the largest address in the address space has fewer significant digits than
this minimum, then the address will only be padded to the size of the largest
address.  If the address has more significant (non-zero) digits than the minimum, it
will be displayed with more digits than the minimum, but will contain no leading
zeros.  This field is disabled and has no effect if the previous "Fully Pad With
Leading Zeros" option  is selected.


**Justification -**This option is used to align the address text to either the left
or right side of the field.  If the text is longer than the space allocated for it in
the field, the text is clipped to the opposite side of the justification.


### Array Options


**Group Array Elements** - Determines whether or not multiple array elements should
be shown on the same line in the browser. If checked, this option will use the **Array**
format, which typically only shows the address, the array index, and the array values.
Note: this only affects arrays with primitive elements. Complex arrays will still only show
one element per line.


**Elements Per Line -** The number of array elements to show on a line. This option
in only enabled if the **Group Array Elements** option is selected.


### Bytes Field


**Byte Group Size** - Bytes in the byte field can be displayed in groups. By default
each bytes are displayed in groups of 1. Groups are separated by delimiters. Use this
setting to change the number of bytes displayed in a group.


**Delimiter -** The string to use to separate groups. Normally, this is set to " " (a
single space).


**Display in Upper Case -** Select this check box if the hex digits of the bytes
should be displayed as ABCDEF instead of abcdef.


**Maximum Lines to Display -** Specifies the maximum number of lines to use to
display the bytes. Any bytes that do not fit into this number of lines will not be
displayed.


**Reverse Instruction Byte Ordering** - The bytes will be displayed in reverse order
for Instruction Code Units. Note: this applies to instructions only. All other code units
are unaffected.


**Display Structure Alignment Bytes** - Internal structure alignment bytes will
be displayed with the bytes of the preceding component.  These bytes will be colored
differently than the bytes directly associated with the component.
Note: this applies to structure data only. All other code units are unaffected.


### **Cursor Text Highlight**


Use the following options to customize [Cursor Text Highlighting](CodeBrowser.md#cursor-text-highlight):


**Enabled -** Select this checkbox to enable cursor text highlighting.


**Mouse Button To Activate** - Use the combo box to select which mouse button will be used
to highlight text (Left, Right, Middle).


**Scope Register Operand** - Check this box to
enable [Scoped highlighting](CodeBrowser.md#scope) of registers within the
operand field. If turned off, cursor highlighted text within an operand field is treated
the same as text in other fields.


**Scoped Default Color -** Sets the color used for cursor text highlighting via
middle-mouse. Double-click on the color bar to bring up a color chooser dialog.


**Scoped Read Highlight Color -** Sets the color used for cursor text highlighting a
register when the register value is read.  The *Scope Register Operand* option
above must be on for this value to be used.
Double-click on the color bar to bring up a color chooser dialog.


**Scoped Write Highlight Color -** Sets the color used for cursor text highlighting a
register when the register value is written to.  The *Scope Register Operand* option
above must be on for this value to be used.
Double-click on the color bar to bring up a color chooser dialog.


### EOL Comments Field


The EOL Comments field displays the end-of-line comment at this address.  By default,
if there is no EOL comment, then other comment types may be displayed.


**Additional Comment Types -** The following comment types may be optionally displayed
in the EOL Comments field.   For each type below, the following setting may be applied:


- **ALWAYS -** Always show the comment type, regardless of other comment types
that are showing.  The appearance of any comment will be limited by the maximum
number of lines currently set on the EOL Comments field.
- **DEFAULT -** Show the comment type only when there is no other comment type
of a higher precedence.  When all fields are set to this option, then the EOL
Comments field will only display one comment type at a time.
- **NEVER -** Do not show this comment type.


Each of the comments below is listed in order of precedence.   The default behavior is to
show one comment in the EOL Comments field at a time, based on this precedence, with the EOL
Comment being the highest.


**Repeatable -** The Repeatable Comment defined *at the current
code unit address*.


**Referenced Repeatable -** The Repeatable Comment that is defined at the
target reference address that the code unit at this address refers to.


**Automatic Function -** A preview of the referenced function.


**Automatic Data -** A preview of the referenced data.  For example, a String
reference will show a preview of the target String.


**Enable Word Wrapping -** If this option is not set, each comment line is displayed
on a line by itself. By turning on word-wrapping, comment lines are displayed in paragraph
form.


**Maximum Lines To Display -** The maximum number of lines to display for a single
comment. Comments that cannot be displayed within this number of lines will be
truncated.


**Prepend the Address to Each Referenced Comment -** Each referenced repeatable
comment will display an annotated address before the comment. This address can be double
clicked to go to the address where that referenced repeatable comment is defined.


**Show Semicolon at Start of Each Line -** Begins each line of an end-of-line comment
with a semi-colon.


**Use Abbreviated Automatic Comments -** When possible, the auto comment will
be made as small as possible.  For example, when showing an offcut string reference,
only the portion of the string that is used will be displayed.


### File Offset Field


The File Offset field shows the filename and file offset of the original imported byte
value for the given address.  If the address's byte was not derived from an imported binary
file, or file offset tracking is not supported by the binary file's importer, no offset is
shown.


**Show Name -** Option to prefix the file offset with the source filename.  This
is useful if more than one binary file has been imported into a program.


**Use Hex -** Option to display the file offset in hexadecimal rather than
decimal.


> **Note:** The File Offset field is disabled by default.
To enable the field, see the Enable Field section.


### Function Offset Field


The Function Offset field shows the function name and function offset of the
the given address.  If the address is not in a function, no offset is shown.


**Show Name -** Option to prefix the function offset with the function name.


**Use Hex -** Option to display the function offset in hexadecimal rather than
decimal.


> **Note:** The Function Offset field is disabled by
default. To enable the field, see the Enable Field section.


### Imagebase Offset Field


The Imagebase Offset field shows the imagebase offset of the given address. If the
address and the imagebase are in different address spaces, no offset is shown.


**Show Name -** Option to prefix the imagebase offset with "imagebase".


**Use Hex -** Option to display the imagebase offset in hexadecimal rather than
decimal.


> **Note:** The Imagebase Offset field is disabled by
default. To enable the field, see the Enable Field section.


### MemoryBlock Offset Field


The MemoryBlock Offset field shows the memory block name and memory block offset of the
given address.


**Show Name -** Option to prefix the memory block offset with the memory block
name.


**Use Hex -** Option to display the memory block offset in hexadecimal rather than
decimal.


> **Note:** The MemoryBlock Offset field is disabled by
default. To enable the field, see the Enable Field section.


### Format Code


Specific formatting of the listing is controlled via the *Format Code* options
panel. The following table describes the effect of each format option. The options for
displaying comments are listed in the order in which the options are processed when
determining what formatting comments are to be displayed. (The order below is based on the
assumption that the order of the comment fields in the Code Browser are
***Plate***, ***Pre***, and ***Post***.)


| **Option** | Field Type | Description |
| --- | --- | --- |
| **Show External Entry Plates** | Plate Comment | Display an "EXTERNAL" plate comment at each label which               is marked as an Entry Point. |
| **Show Function Plates** | Plate Comment | Display a "FUNCTION" plate comment at the entry point of               each Function. |
| **Show Subroutine Plates** | Plate Comment | Display a "SUBROUTINE" plate comment at each label which               has a call reference to it. |
| **Show Transition Plates** | Plate Comment | Display an empty plate comment when transitioning from               between Instructions and Data. |
| **Flag Function Entry** | Pre Comment | Display the pre comment: \|\|\|\|\|\|\|\|\| FUNCTION \|\|\|\|\|\|\|\|\| at the entry point of each Function. |
| **Flag Function Exits** | Post Comment | Display the post comment: **********MyFunctionExit ********** at the end of each Function, where *MyFunction* is the name of the Function. |
| **Flag Jumps and Returns** | Post Comment | Display a post comment "- - -" line separator following               all unconditional jumps and returns. |
| **Flag Subroutine Entry** | Pre Comment | Display the pre comment: \|\|\|\|\|\|\|\| SUBROUTINE \|\|\|\|\|\|\|\| at each label which has a call reference to it. |
|   |   |   |
| **Lines After Basic Blocks** | Post Comment | Display the specified number of blank lines following               all Basic Blocks of instructions. |
| **Lines Before Functions** | Plate Comment | Display the specified number of blank lines before each               Function entry point. (Has precedence over **Lines Before Plates** .) |
| **Lines Before Labels** | Plate Comment | Display the specified number of blank lines before each               labeled code unit (instruction or data). |
| **Lines Before Plates** | Plate Comment | Display the specified number of blank lines before each               plate comment inserted during formatting. (Has precedence over **Lines Before               Labels** .) |


> **Note:** If comments already exist in the listing,
then the options to show the comments fields for formatting are ignored. The options that
specify a number of blank lines are used regardless of whether comments exist.


> **Note:** Applying the format options does not alter
the program.


### Function Pointers


**Display Function Header for External Function Pointers -** Select this option to show
the function prototype header within the listing for any pointer which has an
External Function reference (enabled by default).


**Display Function Header for Non-External Function Pointers -** Select this option to show
the function prototype header within the listing for any pointer which has a
memory reference to a Function (disabled by default).


### Function Signature Field


**Display Namespace -** Select this option to include
the function namespace as a prefix to the name of the function
within the displayed function prototype (disabled by default).


### Labels Field


**Display Function Label -** Select this option to show function labels. If you turn
this off, the function name will only appear in the function signature. If it's on, the
function name will also appear as a label below the function header.


**Display Non-local Namespace -** Select this option to prepend the namespace to all
labels that are not in the current Function's namespace.  Currently, this would only
affect a label that is not global, but is in a namespace other than the function that
contains the label's address.


**Display Local Namespace -** Select this option to prepend the namespace to all
labels that are in the Function's namespace.


Use Local Namespace Override - Select this
option to show a fixed prefix for local labels instead of the function's name.  This
option is only available if the "Display Local Namespace" option is on.  The text box
contains the prefix to use for local labels.


### Mnemonic Field


**Show Data Mutability -** Option to display the mutability data setting associated
with each data code unit (e.g., constant, volatile).


**Underline Fields With Non-primary References -** Option to underline mnemonic
fields that have hidden (non-primary) references. This provides a quick visual indication
that the field has references and that you can double-click the field to go to the
references.


### Operands Field


**Add Space After Separator -** Option to add an additional space after the operand
separator ","


**Always Show Primary Reference -** Option to force the display of the primary
reference on all operands.  If a suitable sub-operand replacement can not be
identified the primary reference will be appended to the operand preceded by a "=&gt;"
prefix.


**Display Abbreviated Deafult Label Names -** Uses a shortened form of the
label name for dynamic String data types in the display of
operand references (e.g., STR_01234567).


**Display Non-local Namespace -** Select this option to prepend the namespace to all
references that are not in the current Function's body.  Currently, this would only
affect a label that is not global, but is in a function other than the function that
contains the current instruction.


**Display Local Namespace -** Select this option to prepend the namespace to all
labels that are in the Function's body.


Use Local Namespace Override - Select this
option to show a fixed prefix for local labels instead of the function's name.  This
option is only available if the "Display Local Namespace" option is on.  The text box
contains the prefix to use for local labels.


**Enable Word Wrapping -** Option to wrap strings in operand lines that are too long
to fit in the operand field. Note that word wrapping can only occur where spaces exist
in the string.


**Follow Read or Indirect Pointer References -** Option to follow referenced pointers,
for read or indirect reference types, to show pointer's referenced symbol instead of
symbol at pointer.  When applied the resulting operand label will be preceded by a
" → ".


**Include Scalar Reference Adjustment -** Option to include a scalar expression which
will indicate the relationship between a replaced scalar and the associated reference
offset when the offset does not match the scalar value.


**Markup Inferred Variable References -** Option to markup instruction operands where
references to stack and register variables can be inferred.  This corresponding
stack/register markup option must also be enabled for this option to have an effect.


**Markup Register Variable References -** Option to markup instruction operands where
explicit register references exist.   When this option is enabled, elements may be
replaced within instruction operands to reflect an association with a register
parameter/variable if one can be determined.   Inferred register references will be
included if the *Markup Inferred Variable References* is also enabled.


**Markup Stack Variable References -** Option to markup instruction operands
where explicit stack references exist.   When this option is enabled, elements may be
replaced within instruction operands to reflect an association with a stack
parameter/variable if one can be determined.   Inferred stack references will be
included if the *Markup Inferred Variable References* is also enabled.


**Maximum Length of String in Default Labels -**
Sets the maximumn number of
characters from a String to include in dynamic String labels in operand references


**Maximum Lines To Display -** The maximum number of lines used to display a string
in an operand. Strings that cannot be displayed within this number of lines will be
truncated.


**Show Block Names** - This option prepends the memory block name to labels in the
operand field. For example, the instruction "call printf"
becomes "call .text:printf".


**Show Offcut Information -** Shows additional information for
[offcut references](../ReferencesPlugin/References_from.md#offcut-references),
such as the original address, followed by the offset.  For example, the
string "foo_bar", with an offcut reference to "bar" would look like:


`
s_bar_12345678+4
`


with this option on, and with it off would look like:

`
s_bar
`


**Underline References -** Option to underline operand references so that you can
quickly identify those operands that have references and double-click to go the reference.
Select one of the following choices:


- *Hidden* - Underline the operand if it has a non-primary reference (i.e. there
is no visible evidence that the operand has a reference.)
- *All* - Underline the operand if it has any references.
- *None* - Do not display any underlines.


> **Note:** You can change the color of the underline
from the Listing Display options panel; select Underline from the Screen Element list.


**Wrap on Semicolons -** Option to wrap operand fields on semicolons. Some processors
have multiple sub instructions encoded at the same address. Normally, these are shown on
one line and the additional instructions are all shown within the operand field and
separated by semicolons. With this option on, each follow on instruction will be displayed
on its own line within the operand field.


### PCode Field


**Display Raw [PCode](../LanguageProviderPlugin/Languages.md#pcode)** -
Option to display the raw PCode directly in the Code Browser (i.e., detailed varnode
specifications are provided).


**Maximum Lines to Display** - The maximum number of lines used to display PCode. Any
additional lines of PCode will not be shown.


### Selection Colors


**Difference Color** - Sets the color used to highlight differences between two
programs.


**Highlight Color** - Sets the Browser [Highlight](../SetHighlightPlugin/Highlighting.md) color.


**Selection Color** - Set the Browser [Selection](CodeBrowser.md#selection) color.


### Source Map Field


**Show Filename Only** -
If selected, only the file name will be shown in the Listing field (rather than the full
path).


**Show Source Info at Every Address** - If selected, source map information will be
displayed for each address in the Listing. Otherwise the source information for a given
source map entry will only be displayed at the minimum address of the corresponding
range.


**Maximum Number of Source Map Entries to Display** - Maximum number of source
map entries to display per address.


**Show Identifier** - If selected, the source file identifier (md5, sha1,...) will
be shown in the Listing.  Note that a source file might not have an identifier.


### Template Display Options


**Max Template Depth** - Sets the depth to display nested templates. A
depth of 0 completely simplifies the entire template, while a depth of 1 will
show 1 level of templates.For example, if the name was "foo&lt;char,bar&lt;int, dog`<char>`&gt;",
a nesting depth of 0 would display "foo&lt;&gt;" and an nesting depth of 1 would display
"foo&lt;char, bar&lt;&gt;&gt;".


**Max Template Length** - This is the maximum length any template string will display.
If the template string exceeds this length, the middle part of the template will be replaced
with "..." to get the string down to the minimum length. For example, the string
"foo&lt;abcdefghijklmnopqrstuvwxyz,0123456789&gt;" would display something like "foo&lt;abcd...6789&gt;"
if the max length was set to 10. Note that this restriction is applied AFTER
any simplifications from the nesting depth.


**Min Template Length** - This is the minimum length of a template before template
simplification is applied. In other words, if the template string is less than this length,
then the template will not be simplified. This is done so that simple templates such as
"foo`<char>`" are not simplified to "foo&lt;&gt;", even if the template nesting depth is set to 0.


**Simplify Templated Names** - This turns the entire templating simplification feature
on or off. If this is off, none of the other option have any effect.


### XREFs Field


**Delimiter -** Delimiter string to use for separating multiple xrefs.


**Display Local Block -** Prepends the name of the memory block containing the XREF
source address to each XREF.


**Namespace Options:**


**Display Non-local Namespace -** Select this option to prepend the namespace to all
XREFs that are not from an instruction within the current Function's body.  Currently,
this would only affect XREFs that originate in some other function.


**Display Library in Namespace -** Include the library name in the namespace.


**Display Local Namespace -** Select this option to prepend the namespace to all
XREFs that are from the current Function.


**Use Local Namespace Override** - Select this
option to show a fixed prefix for local XREFs instead of the function's name.  This
option is only available if the "Display Local Namespace" option is on.  The text box
contains the prefix to use for local XREFs.


**Display Reference Type -** Shows a single letter to represent the type of reference.
Some of the possible types are:
`Read (R), Write (W), Data (*), Call (c), Jump (j) and Thunk (T)`.



**Group by Function -** Groups all references by the containing source function.
With this option off, all references within a function are displayed on their on row.
With this feature on, each function will get a single row, with all references displayed on
that row.



**Maximum Number of XREFs To Display -** The maximum number of lines used to display
XREFs. Additional XREFs will not be displayed.


**Sort References by -** Allows the references to be sorted by Address or by type.
This is most useful when **Group by Function** is off.


## Popups


Popups are transient windows used to display additional information about the item over
which the mouse is hovering. There are options for enabling various types of popups and for
resizing the popup window.


### **Listing Popups**


To view or change the available popups, open the [Tool Options Dialog](../Tool/ToolOptions_Dialog.md) and then select the
*Listing Popups* node in the Options tree.


**Reference Code Viewer -** Shows the listing at the referenced location as a
popup.


**Truncated Text Display -** Displays truncated text as a popup.


### **Reference Code Viewer**


To view or change the size of popup windows, open the [Tool Options Dialog](../Tool/ToolOptions_Dialog.md) and then open the
*Listing Popups* node in the Options tree. Next select the *Reference Code
Viewer* node.


**Dialog Height -** The height of the popups in pixels.


**Dialog Width -** The width of the popups in pixels.


---

[← Previous: Cursor Text Highlight](CodeBrowser.md) | [Next: Program Differences →](../Diff/Diff.md)
