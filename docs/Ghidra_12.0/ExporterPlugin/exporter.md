[Home](../index.md) > [ExporterPlugin](index.md) > Export Program

# Exporting Files


Ghidra provides an *Exporter* that allows a user to output program information into a
file in various formats.


Some of the formats the *Exporter* supports are:


- [ASCII](#ascii)
- [C/C++](#c-cpp)
- [Ghidra Zip File (GZF)](#gzf)
- [Ghidra Data Type Archive File (GDT)](#gdt)
- [HTML](#html)
- [Intel Hex](#intel-hex)
- [Original File](#original-file)
- [Raw Bytes](#binary)
- [XML Export Format](#xml)
- [SARIF Export Format](#sarif)


## Export Action


The export action can be invoked from the front-end project window or the CodeBrowser
tool.


### To export from the front-end project window:


#### Steps:


- Right-click on the file to export in the tree.
- From the popup menu that appears, select the **Export...** menu item.
- Use the [Exporter Dialog](#exporter-dialog) that appears to configure the
export.
- Press the **OK** button to perform the export.


*In preparation for a file export, a selected project
file may be opened in an attempt to support export formats that require an open
file.  If the selected file requires an upgrade a warning dialog
will be displayed and the affected export formats will not be available until an upgrade
is perfored, however a direct packed format of the project file may still be chosen
without performing the upgrade first (e.g., [Ghidra Zip File (GZF)](#gzf),
[Ghidra Zip File (GZF)](#gzf)).*


### To export from the CodeBrowser tool:


#### Steps:


- Make sure the program to export is the currently open program in the CodeBrowser
tool.
- Invoke the action from the **File → Export
File...** menu item.
- Use the [Exporter Dialog](#exporter-dialog) that appears to configure the
export.
- Press the **OK** button to perform the export.


## Export Dialog


The Export Dialog is used to configure the export of the chosen program.


![](images/Export_Dialog.png)


### Dialog Fields


- **Format** - This field is a drop-down list containing all the valid [export file formats](#exporter-formats) that could be used to export the
program. By default, the last used format will be auto-selected.
- **Output File** - This field specifies the output file for the export. By
default, the output file's name will be the name of the program and the output folder
will be the user's home folder or the last folder used for an export if an export has
been performed in the current session. Use the "..." button to bring up a file chooser
to change the output file.
- **Selection Only** - If this checkbox is selected, then only the areas of the
program that are in the current selection will be exported. Obviously, this only
applies when exporting from an open program with a selection in the CodeBrowser tool
and not when exporting from the front-end project window. Also, not all export formats
support partial exports. The GZF format, for example, always exports the entire program
since it is really just making an exported copy of the entire program database.
- **Options...** - This button will pop up format specific options for the
import.


## Exporters


### Ascii


Creates a plain text representation of the program's listing, similar to what is
displayed in the [Code
Browser Field Format](../CodeBrowserPlugin/Browser_Field_Formatter.md).


#### Ascii Options


![](images/Ascii_Options.png)


#### Advanced


| *Label Suffix*   | the string to append on the end of labels   |
| --- | --- |
| *Comment Prefix*   | the string to prepend to the beginning of comments   |


#### Show


The check-boxes in this panel are used to determine what program elements should
be included in the output file. A selected check-box denotes that the corresponding
element will be included in the file. The checkboxes for elements that are present in
the program are selected by default.


| *Comments* | Include *Pre* , *Post* , *EOL* , and *Plate* comments |
| --- | --- |
| *Properties* | Include properties; e.g., *Bookmarks* , *Spacers* |
| *Structures* | Include *Structures* and *Unions* defined on code units |
| *Undefined Data* | Include all undefined code units (e.g, "??") or                     replace with " *[BYTES REMOVED]* " place-holder |
| *Ref Headers* | Include the cross reference header *BACK[m,n]* or *FWD[m,n]:* , where *m* is the number of cross                     references and *n* is the number of offcut cross reference; select the **Back Refs** and/or *Forward Refs* for the *Back/FWD* header to show up |
| *Back Refs* | Include the list of cross references for each                     code unit |
| **Forward Refs** | Include the list of references to the mnemonic                     for each code unit |
| *Functions* | Include signature and header for each                     function |


#### Width


The text-fields in this panel specify the width, in number of characters, to use
when displaying program elements in the output file.


> **Note:** Setting a width to zero (0)
effectively excludes it from the output file.


### C/C++


Create a C/C++ file containing functions decompiled from the program and, optionally,
containing definitions of all datatypes from the program's
[data type manager](../DataTypeManagerPlugin/data_type_manager_description.md). The datatype definitions and a prototype declaration for each function
can be placed in a separate header file.


#### C/C++ Options


![](images/C_Options.png)


- **Create Header File (.h)** - Select to create a .h file.
- **Create C File (.c)** - Select to create a .c file.
- **Use C++ Style Comments (//)** - Select to use // or /* style comments.
- **Emit Data-type Definitions** - Select to export a C/C++ definition for each data-type.
- **Emit Referenced Globals** - Select to export a C/C++ declaration for referended global variable.
- **Function Tags to Filter** - Optional list of function tags to filter which
functions are exported. Multiple tags must be comma separated.   Any tags listed will
be considered a match for purposes of filtering.  The result of filtering, to include
or exclude, depends on the **Function Tags Excluded/Included** setting.
If this list is empty, than all functions will be exported.
- **Function Tags Excluded/Included** - Select to exclude from export all
functions with a tag that matches any in the **Function Tags to Filter** list.
Deselect to include in export only functions with a tag that matches any in the list.


### Ghidra Zip File (GZF)


Creates a GZF file from a Program in your project. You may want to create a GZF file
so that you can give it to another user who can then [import](../ImporterPlugin/importer.md) into their project.  A program
export of this format from the Project Window will be based on the current saved file
content and bypass any potential upgrade that may be required by other formats.


### Ghidra Data Type Archive File (GDT)


Creates a GDT file from a Data Type Archive in your project. You may want to create a GDT file
so that you can give it to another user who can then [import](../ImporterPlugin/importer.md) into their project or open directly
via the Data Type Manager as a
[File Data Type Archive](../DataTypeManagerPlugin/data_type_manager_description.md#open-file-data-type-archive).
A project Data Type Archive export of this format from the Project Window will be based on
the current saved file content and bypass any potential upgrade that may be required by other formats.


### HTML


Creates a hyper-text representation of the program's listing, similar to what is
displayed in the [Code
Browser Field Format](../CodeBrowserPlugin/Browser_Field_Formatter.md). The HTML output is analogous to the ASCII output, however HTML
allows format and hyper-link information to be added to the file. The formatting allows
fields to be color-matched to those in the Code Browser. The hyper-linking allows
navigation similar to that supported in the Code Browser.


*The HTML Options are identical
the [ASCII Options](#ascii-options).*


### Intel Hex


The Intel Hex format, a printable file representing memory images, was originally
designed to program EPROM devices. The Intel Hex exporter creates files in this format
which can be used to program these EPROM devices.


#### Intel Hex Options


![](images/Intel_Hex_Options.png)


- **Address Space** - Specifies which address space to export as Intel Hex format
only supports one address space. This option will be initialized to the "default"
address space.
- **Record Size** - Specifies the size (in bytes) of each record in the
output file. The default 16.
- **Align To Record Size** - If checked, this will ensure that **only** records matching
the record size will be output. eg: if you set the record size to 16 but there are
18 bytes selected, you will see only one line of 16 bytes in the output; the remaining
2 bytes will be dropped.


### Original File


Writes a program back to its original file layout. By default, any file-backed bytes
that were modified by the user in the program database will be reflected in the new file.
Optionally, the program can be written back to its unmodified file bytes, discarding all
user modifications.


#### Original File Options


- **Export User Byte Modifications** - If checked, user byte modifications are
preserved in the exported file. If unchecked, no user byte modifications are preserved
and the exported file will exactly match the file that was originally imported.


- **Save Multiple File Sources To Directory** - If checked, the destination file
will be treated as a directory. Each file source from the program will be saved to this
newly created directory with names of the form `<directory>`.0, `<directory>`.1,
etc. If the program contains multiple file sources and this option is not checked, only
the primary (first) file source will saved to the specified destination file.


> **Note:** This exporter is only
operational when the program has at least one file-backed byte source.  This will be
reflected in the Memory Map's Byte Source column, which entries that begin with File:


> **Note:** Writing back a modified Memory
Map is not supported.


> **Note:** Relocation bytes are always
restored to their original values, even if the user modifies them.


> **Warning:** Programs written to disk with
this exporter may be runnable on your native platform.  Use caution when exporting
potentially malicious programs.Raw Bytes


Creates a binary file containing only the raw bytes from each memory block in the
program. If there are multiple memory blocks, their bytes will be concatenated in the
exported binary file.  If the program was originally created using the **Binary
Importer** and there is only one memory block, then this exporter allows recreation of
the original file.


> **Note:** Only initialized memory blocks
are included in the output file.


### XML


The XML Exporter creates XML files that conform to Ghidra's Program DTD. You can
re-import files in this format using the [XML Importer](../ImporterPlugin/importer.md).


*The
XML Options are identical the [XML Importer Options](../ImporterPlugin/importer.md#xml-options).*


### SARIF


The SARIF Exporter creates SARIF files that conform to Ghidra's Program DTD. You can
re-import files in this format using the [SARIF Importer](../ImporterPlugin/importer.md).


*The
SARIF Options are identical the [SARIF Importer Options](../ImporterPlugin/importer.md#sarif-options).*


**Related Topics:**


- [Importing Files](../ImporterPlugin/importer.md)


---

[← Previous: Batch Import](../ImporterPlugin/importer.md) | [Next: Open Program →](../ProgramManagerPlugin/Opening_Program_Files.md)
