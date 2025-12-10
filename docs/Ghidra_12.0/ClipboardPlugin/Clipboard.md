# Clipboard


Ghidra includes clipboard support so that data and code can easily be transferred in and out
of your project. The Ghidra clipboard supports copying and pasting in a variety of formats
(achieved by executing the [*Copy Special...*](#copy-special) command). Each
window defines its own behavior for how the clipboard will function and what types of data will
be copied.


The Code Browser supports the following copy formats:


- [Labels and Comments](#listing)
- [Formatted Code](#listing)
- [Byte String](#listing)
- [Byte String (no spaces)](#listing)
- [GhidraURL](#listing)


The default copy operation in the Code Browser (achieved by executing the [*Copy*](#copy) command), however, will copy either selected text or the specific field
under the cursor, depending upon the current selection and cursor location in the browser.


- If there is a selection, then that selection's text will be copied.
- If there is no selection, then a copy **may** take place, depending upon the field under
the cursor (this works for the Code Browser only). The following list of fields support
copying:
  - Operand Field Reference
  - Label Field
  - Comment Field
  - Address Field
  - Bytes Field


To do the default copy, make a selection in the Code Browser, right mouse click and choose
the **Copy** option.


In order to copy labels and comments, right-click from within the Code Browser, Click
***Copy Special...***, and choose the format you would like to copy. The last selected
format is also available from the right-click popup menu.


The clipboard supports the following operations:


- ***Copy*** - Copies selected items onto the clipboard.
- ***Paste*** - Pastes the clipboard contents to the current location.
- ***Copy Special...*** - Allows for a copy operation where the type/format copied
is specified by the user.


The clipboard allows for data to be both copied locally (within Ghidra) or onto the system
clipboard. Data copied onto the system clipboard may be accepted by other applications.


## Default Operations


### Copy ![page_white_copy.png](../icons/page_white_copy.png)


Copies the currently selected items. The behavior will be dependent on the specific window
you copy from. Generally, copy means to place a copy of whatever is selected onto the
clipboard so that it can be pasted in another location within Ghidra or to another
application. The copy action can be triggered via the context menu that appears when you
right-click.


### Paste ![page_paste.png](../icons/page_paste.png)


Pastes the clipboard contents to the current location. The behavior will be dependent on
the specific window you paste to. Generally, paste means to insert a copy of whatever is on
the clipboard to the location the cursor is currently at. Unlike the cut and copy actions,
the paste action is always enabled because it cannot be notified of clipboard changes. If you
attempt to paste and the data on the clipboard is not compatible with the window you pasted
in, you will receive an error message. The paste action can be triggered via the context menu
that appears when you right-click.


## Custom Operations


### Copy Special


![](images/CopySpecial.png)


The copy special dialog allows you to copy the selected information in a specific format.
You can trigger the copy special dialog via the context menu that appears when you
right-click. When the dialog appears, it will contain a list of the currently available
formats. Choose the format you want and click **OK** to copy the selected information to
the clipboard.


The last selected format from the copy special dialog will appear on the popup menu along
with the standard copy and paste operations (it is only visible when the last selected format
is applicable). This feature allows you to repeatedly copy the same format quickly from
either the menu or by binding a key to it. To specify a key binding, select **Edit** → **Tool Options**, click on `Key Bindings`,
and choose the action for which you want to define a key. The action for repeat copying of
the last format is called `Copy Special Again`. When available, the popup menu
appears as follows:


![](images/CopySpecialAgain.png)


## Supported Windows


### Listing


The Code Browser **Listing** window can copy the following formats:


- **Formatted Code<a name="formattedcode"></a>** - Copies text from the selected
blocks in the Code Browser to the clipboard. The spacing and formatting are preserved as
much as possible. The plain text can easily be pasted into a text processor. **This is the
default copy format**.
- **Labels and Comments** <a name="labelscomments"></a> - Copies the labels and
comments from the selected blocks in the Code Browser to the clipboard. These can be pasted
to another part of the program or to another open Code Browser, however, there is no
external application that will paste the labels and comments. If you are pasting labels at
a location where a default label exists, then the default label will be removed. Also, a
default label cannot be pasted. Trying to paste a default label will result in no
change.
- **Byte String<a name="bytestring"></a>** - Copies the bytes from the selected blocks
in the Code Browser to the clipboard as text. These can be pasted to another part of the
program (provided the area pasted to is undefined) or to an external application that
supports pasting byte strings. Often, hex editors will be able to paste this format.
- **Byte String (No Spaces)** <a name="bytestring-nospaces"></a> - This is the same as
the Byte String format, except there are no delimiting spaces between bytes.
- **Data** - Copies a the values of all the selected data objects to the clipboard as
text. This option ignores any compound data objects such as structures, unions, or arrays.
You can copy data from structures, but you must first open them and select the elements you
want to copy as a string.
- **Dereferenced Data** - Copies the values of all data pointed to by the selected
pointers. The contents will be copied to the clipboard as text. If the pointed to data is a
compound data object such as a structure or array, it is ignored.
- **Python Byte String** - Copies the bytes into the Python byte string format, for
example: `b'\x41\xec\x49\x89'`.
- **Python List String** - Copies the bytes into the Python list format, for
example: `[ 0x66, 0x2e, 0x0f, 0x1f, 0x84 ]`.
- **C Array String** - Copies the bytes into the C array format, for
example: `{ 0x66, 0x2e, 0x0f, 0x1f, 0x84 }`.
- **Address** - Copies the address at the top of the selection.
- **Address w/ Offset** - Copies the address at the cursor or each address in the
current selection.   The text is formatted to show the offset from the entry point of the
function, for example: `main + 0x2`
- **Byte Source Offset** - Copies the byte source offset from the start of the file for
each address in the current selection. If the address is not backed by a file,
`<NO_OFFSET>` is copied.
- **GhidraURL** <a name="ghidraurl"></a> - Creates a GhidraURL for the address under the
cursor then copies that URL to the clipboard.


The Code Browser **Listing** window can paste the following formats:


- **Labels and Comments** - Labels and comments can be pasted anywhere in the
program.
- **Byte String** - Any string of text bytes can be pasted into an undefined region of
the program. White space will be ignored.
- **Label String** - Available when a default copy was performed while there was no
text selection. This value can be pasted onto a label or comment.
- **Comment String** - Available when a default copy was performed while there was no
text selection. This value can be pasted onto a comment.
- **Byte String** - Available when a default copy was performed while there was no
text selection. This value can be pasted onto a comment.
- **Address String** - Available when a default copy was performed while there was no
text selection. This value can be pasted onto a comment.


The paste is able to determine the type of data on the clipboard and will paste the
appropriate type when it is triggered.


### Bytes in Memory


The Byte Viewer **Bytes In Memory** window can copy the following formats:


- **Byte String** - Copies the bytes from the selected blocks in the Code Browser to
the clipboard as text. These can be pasted to another part of the program (provided the
area pasted to is undefined) or to an external application that supports pasting byte
strings. Often, hex editors will be able to paste this format. **This is the default copy
format**.
- **Byte String (No Spaces)** - This is the same as the Byte String format, except
there are no delimiting spaces between bytes.
- **Python Byte String** - Copies the bytes into the Python byte string format, for
example: `b'\x41\xec\x49\x89'`.
- **Python List String** - Copies the bytes into the Python list format, for
example: `[ 0x66, 0x2e, 0x0f, 0x1f, 0x84 ]`.
- **C Array String** - Copies the bytes into the C array format, for
example: `{ 0x66, 0x2e, 0x0f, 0x1f, 0x84 }`.


The Byte Viewer **Bytes In Memory** window can paste the following formats:


- **Byte String** - Any string of text bytes can be pasted into an undefined region of
the program. White space will be ignored.


The paste is able to determine the type of data on the clipboard and will paste the
appropriate type when it is triggered.
