# Program Options Dialog


A program has properties that may be edited with an *Options* dialog. The dialog is
used just like the [Tool Options](../Tool/ToolOptions_Dialog.md) dialog
except that the properties are saved as part of the Program, versus part of the tool.
Properties are settings related to a program.


<a name="optionssampleimage"></a>


![](images/ProgramOptionsDialog.png)


## Accessing Program Properties


The Program Options dialog allows the user to control various settings related to a
program.  The settings are organized into categories and are viewed with the Program
Options Dialog.  The category hierarchy is displayed on the left side, while individual
settings for the selected category are displayed on the right.  See below for detailed
information on the various settings.


Generically, to modify a program option or setting for the currently open
program:


1. Select **Edit →  Program
Options...**.
2. Select the *category* node in the Options tree to view the settings
for that category.
3. The displayed settings can then be changed as needed.
4. Select **OK** to dismiss the dialog, or **Apply** to make the changes
but leave the dialog displayed.


## Detailed Properties Descriptions


Except for the Program Information category, all other categories are created
by plugins.  Depending on what has previously been done to the program, your settings may
differ from those shown.  However, the Program Information category is always present and
shows basic information about the program.  The following is a description of the
categories and settings you may encounter:


| Program Information Options |  |  |
| --- | --- | --- |
| Executable Format | The binary file format of the executable. (e.g. Portable Executable, ELF,           DOS MZ, etc.) |  |
| Executable Location | The absolute path of the executable binary. |  |
| Analysis/Bytes Options | Aggressive Instruction Finder (Prototype) |  |
| Create Address Tables | Locates address jump tables and follow flow. |  |
| Disassemble Entry Points | Disassemble from all external entry points. |  |
| Library Identification Analyzer | Attempts to match function signatures to standard libraries |  |
| Analysis/Bytes/Create Address Tables Options | Minimum Table Size | Minimum number of addresses required to constitute a valid jump           table |
| Table Alignment | Alignment boundary for valid addresses. |  |
| Analysis/Bytes/Library Identification Analyzer | Analyze undefined memory | Examines undefined bytes attempting to locate library function signatures           that may dynamically invoked. |
| Disassemble matches in undefined memory | Disassembles matching code when analyzing undefined memory |  |
| Analysis/Disassembly | Mark Bad Disassembly | Flag locations where code was expected but could not be           disassembled. |
| Analysis/Functions | Decompiler Stack Analysis |  |
| Stack Analysis |  |  |
| Analysis/Instructions |  |  |
| Data Reference Analysis |  |  |
| Scalar Operand References |  |  |
| Subroutine References |  |  |
| Analysis/Instructions/Data Reference Analysis | Ascii String References | Searches for ascii strings and labels them with an "s_" prefix |
| Subroutine References |  |  |
| Unicode String References | Searches for unicode strings and labels them with an "u_" prefix |  |


## Property Editors


In addition to the editors for modifying boolean values, fonts, colors, etc., Ghidra
provides editors for changing dates and filenames.  These editors are described in the
following paragraphs.


### Date Editor


The [sample image](#program-options-dialog) above shows an option for *Date
Created*. Click on the browse button (**...**) to the right of the field that shows
the date. The date editor is displayed as shown below.


![](images/EditDate.png)


The editor displays a calendar to change the month, day or year, and
separate fields to edit hours, minutes, and seconds. The scroll bar next to the seconds
fields pertains to the current field that you are editing, as indicated by the purple
background. In the sample image, the seconds field is the current field; if you click on
the up arrow,  the seconds field is incremented.


After you have made your changes, click on the **OK** button. The date
field on the options panel updates to show the new date. The **Apply** button becomes
enabled. Click on either the **OK** or **Apply** button to make the change.


### File Chooser Editor


If a property is a filename, then it can be edited using the *File Chooser* editor.
Click on the browse button (**...**) to the right of the field that shows the filename.
A file chooser is displayed. Select the new filename from the file chooser and click on
either the **OK** or **Apply** button to make the change.


*Provided by: *ProgramManagerPlugin**


**Related Topics:**


- [Tool
Options](../Tool/ToolOptions_Dialog.md)
