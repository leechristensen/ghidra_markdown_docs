[Home](../index.md) > [EquatePlugin](index.md) > Binary

# Equates


An Equate is a string substitution for [scalar](../Glossary/glossary.md#scalar) (a numeric value) in any code unit
(instruction operand or data). For example, consider the instruction below:


`MOV R2, $0xb`


The scalar *$0xb* can be replaced with the string *BATTERY_FLAG_CRITICAL*. This
will yield the following:


`MOV R2, BATTERY_FLAG_CRITICAL`


The substitution of "BATTERY_FLAG_CRITICAL" for *$0xb* is called an equate. That is,
*$0xb* is equated to "BATTERY_FLAG_CRITICAL". Note that the default choice for the new
equate application is your current location. "BATTERY_FLAG_CRITICAL" will replace the scalar
value *$0xb* only at the current cursor location unless you choose a different option.
However, when replacing another scalar of the same value, a list of previously declared Equates
for that scalar value is presented.


Scalars can only be equated to strings. The string can be of any length and may contain
spaces and special characters. Duplicate equate names are not allowed.


> **Note:** It should be noted that for the purposes of
this document, "scalars" refers to scalar values contained in code units . A code unit
is an instruction operand or other data element.


There are several operations that are associated with Equates. They are:


- [Set Equate](#set-equate)
- [Rename Equate](#rename-equate)
- [Remove Equate](#remove-equate)
- [Apply Enum](#apply-enum)
- [View Equates](#view-equates)
- [Convert](#convert)


## Set Equate


The *Set Equate* action will create one or more Equates in the Listing.


To set an Equate:


1. Right-mouse-click on the target scalar value**,** and select **Set Equate** or
press **`<E>`**.
![Set Equate Dialog](images/SetEquate.png)
2. When the dialog appears, either type in an equate string or choose one from the list of
strings that are known to be associated with the given value. As you type in the "Equate
String" fi1eld, the list will be narrowed down to show only the strings that contain the
text that has been typed.
3. Select one of the choices from the "Apply To" list. **Current Location** is the
default choice unless a selection is made, in which case the **Current Selection**
option will be set. The other option is **Entire Program.**
1. **Current Location**: When selected the equate will be applied to the scalar
value at the current location of your cursor only.
2. **Current Selection**: When selected the equate will be applied to all of the
scalar values in your current selection that match the value of the scalar that you
originally clicked. When you make a selection in your program this button will become
enabled. If you do not make a selection then it will not be enabled and the option will
be grayed out. Note that scalars in your selection that already have an equate set will
not be affected by this unless you also select the overwrite option.
3. **Entire Program**: When selected the equate will be applied to all of the
scalar values in the entire program that also match the value of the scalar that you
originally right-mouse-clicked on.
4. **Overwrite existing equates**: This option is only enabled when setting equates
in a selection or the whole program. If this option is selected, all scalars and all
named equates in the selection or entire program, depending on which option is
selected, will be set with the user-given equate name. If the overwrite option is not
selected, only scalars not already with equates set will be assigned the user-given
equate name.
4. Double-click on an entry in the list, or select an entry in the list and press
**OK**, or type in the string and press OK. If any item in the list is selected it will
be used, otherwise the text in the "Equate String" field will be used.


> **Note:** The list of strings shown in the Set
Equate dialog are generated from two sources. The first source is all the currently
assigned equates to the given value. The other source is all the Enum datatypes that exist in
all the open datatype archives. If an Enum datatype exists that has a member value
equal to the given equate value, then that string will be included.


> **Note:** The open data type archives contain
valid enums and "fake" enums. The fake enums are created from #define values (parsed from .h
files), specifically so that they will be available in the Set Equate dialog./P>


> **Note:** Each entry in the dialog is color-coded based
upon how it is being used as an equate.


1. **Blue**: Blue entries are existing user-defined string equates that are being used
for that scalar.
2. **Black**: Black entries are existing enum field equates being used for that
scalar.
3. **Gray**: Gray entries are suggested enum fields that have the same value as the
scalar. These entries are only suggestions, and have not yet been made equates.


## Rename Equate


The *Rename Equate* action will rename one or more instances of a named Equate in the
Listing.


To rename an Equate:


1. Right-mouse-click on the current Equate**,** and select **Rename Equate** or press
**`<E>`**.
![Rename Equate Dialog](images/RenameEquate.png)
2. Select one of the choices from the "Apply To" list. **Current Location** is the
default choice unless a selection is made, in which case the **Current Selection**
option will be set. The other option is **Entire Program.**
1. **Current Location**: When selected the equate will be applied to the scalar
value at the current location of your cursor only.
2. **Current Selection**: When selected the equate will be applied to all of the
scalar values in your current selection that match the value of the scalar that you
originally clicked. When you make a selection in your program this button will become
enabled. If you do not make a selection then it will not be enabled and the option will
be grayed out.
3. **Entire Program**: When selected the equate will be applied to all of the
scalar values in the entire program that match the value of the scalar that you
originally clicked. Scalars that already have an equate set that is different from the
one you selected will not be affected.
3. Double-click an entry in the list, select an entry in the list and press **OK**, or
type in the string and press **OK**. If any item in the list is selected it will be
used, otherwise the text in the "Equate String" field will be used.


## Remove Equate


The *Remove Equate* action will remove an Equate(s) from a listing; effectively
returning the operand to its original scalar value.


To remove references to an Equate via the context popup menu:


1. Right-mouse-click on an existing Equate, or select a group of equates and right-click
on an equate within that selection, then choose **Remove Equate** or press
&lt;**Delete**&gt;.
2. If you made a group selection, a confirmation dialog will appear to ensure you want to
remove all equates in the selection; equates within the selection matching the one you
clicked will be removed.
![Confirm Equate Remove Dialog](images/RemoveSelection.png)


To remove all references of an Equate via the *Equates Table* window:


1. Select the Code Browser menu option **Window → Equates Table** to bring up the *Equates Table* window.
2. Right-mouse-click on the Equate to be deleted and select **Delete**.
3. A confirmation dialog will appear.
![Confirm Equate Delete Dialog](images/ConfirmEquateDelete.png)
4. Select **Delete** to remove all references to the equate and the Equate's definition
itself.


## Edit Enum


The *Edit Enum* action is available from the *Equates Table* window.
Right-mouse-click on an existing Equate in the table.  If that equate is part of an enum,
then this action will show the enum in an editor window.


## Show Enum


The *Show Enum* action is available from the *Equates Table* window.
Right-mouse-click on an existing Equate in the table.  If that equate is part of an enum,
then this action will show that enum in the Data Type Manager window.


## Apply Enum


The *Apply Enum* action (only available when there is a selection), will apply enum
member names to scalars in the current selection if any of the enum values match those
scalars.


To apply an enum to the selection:


1. Make a selection and then Right-mouse-click, then choose **Apply Enum**.
![Apply Enum Popup](images/BeforeApplyEnum.png)
2. A dialog similar to the one below should appear. Select the enum that you want to be
applied to the selection. The data type must be an enum for the action to work.
![Apply Enum Popup](images/ApplyEnum.png)
- *Apply to sub-operands* - Applies the enum to scalars within operands.
Once the data type is selected, the scalars in the selection will have equates applied
to them as shown below.
![Apply Enum Popup](images/AfterApplyEnum.png)


## View Equates


The *Display Equates Table* action displays a window which lists all of the Equates
and their references in a tabular format.


![Equates Table](images/EquatesTable.png)


The left panel, *Equates,* lists name, value, and number of references for all
Equates. The right panel, *References,* lists the address and operand index of each
location that references the Equate selected in the left panel. Selecting an address on the
*References* panel will cause the Code Browser to go to that address in the listing. The
*Equates* panel and the *References* panel can each be sorted by any column. The
ascending and descending indicator displays the sort order of the information.


To view the *Equates Table* select the Code Browser menu option **Window → Equates Table** to bring up the *Equates Table*
window.


You can re-order the columns in the Equates table by dragging the header to another
position in the table. Sort the columns by double-clicking on the header. By default, equates
are sort alphabetically. You can re-order the References table and sort by the operand index,
Op Index. By default, the references are sorted by reference address in ascending order.


You can rename an equate by double-clicking the name field and entering a new
name. If the equate is based off of an enum, then double-clicking will not trigger an edit.
Instead, you can right-click and edit the containing enum. In the enum editor, changing
the matching field name will also change the equate name.


> **Note:** Each equate is color-coded based upon how it
is being used.


1. **Blue**: Blue equates are existing user-defined string equates that are being
used for that scalar.
2. **Black**: Black equates are existing enum field equates being used for that
scalar.
3. **Red**: Red entries are bad equates. A bad equate could either mean that the enum
that this equate is based off of was deleted, the field inside the enum was deleted, or
the field's value was changed.


## Convert


The various convert actions are used to change the number format display of scalars
displayed in the code browser. These actions are available whenever the cursor is on a number
in the operand field, or the value field of a data item (byte, word, dword, qword). Note that
these actions and equates are not currently supported for composite and array data. For
instruction operands, the scalar number is converted visually by replacing the number with an
appropriately named equate. Such a conversion can be cleared by removing the equate from the
operand. For data value fields, a combination of data format settings and signed/unsigned data
type alteration is used to reflect a conversion. The available formats are as follows.


### Signed Decimal


The existing scalar value will be displayed as a signed decimal number. This action is
only available if the value can be interpreted as a negative value.


### Unsigned Decimal


The existing scalar value will be displayed as an unsigned decimal number. If the value
would be positive even if the signed decimal format was selected, the action will simply be
name **Decimal** instead of **Unsigned Decimal**.


### Unsigned Octal


The existing scalar value will be displayed as an unsigned octal number.


### Signed Hex


The existing scalar value will be displayed as a signed hexadecimal number. This action is
only available if the value can be interpreted as a negative value, and is only supported on
instruction operands since the data hex format currently supports unsigned rendering
only.


### Unsigned Hex


The existing scalar value will be displayed as an unsigned hexadecimal number.


### Char / Char Sequence


The existing scalar value will be displayed as either a single ASCII character or a
sequence of ASCII characters, whichever is more appropriate. Invalid and non-printable ASCII
characters will be rendered in hex (e.g., \x20).


### Unsigned Binary


The existing scalar value will be displayed as an unsigned binary number.


### Float


The existing scalar value will be displayed as a IEEE 754 single precision floating point
number. The floating point size is processor specific and will match the size of the Float
data type. This action is only supported on instruction operands.


### Double


The existing scalar value will be displayed as a IEEE 754 double precision floating point
number. The floating point size is processor specific and will match the size of the Double
data type. This action is only supported on instruction operands.


> **Tip:** The convert actions also work on an
instruction selection. Just make a selection then choose an operand scalar value to convert.
All matching instruction scalar values in the selection will be converted.


> **Tip:** Based upon how an instruction is
implemented by its' associated language module, a hexadecimal operand which appears to be
negative may in fact be a positive scalar with negative sign '-' character prepended. In such
cases, the convert action may not produce the expected result.


> **Tip:** The presence of a primary reference on
an operand may prevent rendering of the converted scalar value since reference markup takes
precedence over equates and data formatting.


*Provided By: *EquatePlugin* and *EquateTablePlugin**


**Related Topics:**


- [Code Browser](../CodeBrowserPlugin/CodeBrowser.md)
- [Data Type Manager](../DataTypeManagerPlugin/data_type_manager_window.md)


---

[← Previous: Char / Char Sequence](Equates.md) | [Next: Functions →](../FunctionPlugin/Functions.md)
