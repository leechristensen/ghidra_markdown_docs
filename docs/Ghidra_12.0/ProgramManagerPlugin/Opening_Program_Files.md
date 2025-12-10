[Home](../index.md) > [ProgramManagerPlugin](index.md) > Open Program

# Opening Program Files


Ghidra Tools can open an existing Ghidra [program](../Program/Ghidra_Programs.md) file and present it for review and
analysis. Programs from other [viewed projects](../FrontEndPlugin/Ghidra_Front_end.md#view-other-projects) or
[viewed repositories](../FrontEndPlugin/Ghidra_Front_end.md#view-a-repository) may also be
opened.


A program can be opened in the currently displayed tool or can be displayed in a [new instance of a Tool](#opening-a-program-in-a-new-tool-via-drag-and-drop).


## Opening a Program File in the Current Tool


1. To open a program file in the currently displayed tool, select **File →  Open...** from the Ghidra Tool's menu.
2. The *Open Program* dialog is displayed.


![](images/OpenProgram.png)


This allows selection of any file that is part of the active project.


1. Select the program file to open.
2. Click the **OK** button *OR* double click on the program to open.


The selected program is opened and displayed in the tool.  More than one program can be opened at the same time, but only one
of them can be *active* at a time. The Code Browser window shows a tab for each
program that you have opened. Select a tab to make that program the active one, as shown in
the image below.


![](images/Tabs.png)


In addition to selecting a file, this dialog can be used to perform some basic
directory/file operations. Right click on a program to get the directory/file menu.


![](images/OpenProgramMenu.png)


### History


The History button on the *Open Program* dialog expands the dialog to show previous
versions of a program (if the selected program is [shared](../Glossary/glossary.md#shared-program)),  allowing the user to
view a read-only previous version of the program.


![](images/OpenHistory.png)


The History panel shows all previous versions for the selected program.  Each entry
shows which user created the version, the date and time the version was created, the version
number, and the comment for that version.  To open a history file, select it in the
Version History table, and press the "OK" button.  The version history can be hidden by
pressing the "No History" button.


## Opening a Program in a New Tool via Drag and Drop


1. Locate the program to open in the Ghidra Project Window.


![](images/FrontEnd3.png)


1. Left mouse press on the program in the tree, drag it to the Tool Chest, and drop it on
the desired tool by releasing the left mouse button.


> **Tip:** The icon in the Tool
Chest indicates the CodeBrowser tool.


1. A new instance of the tool is launched with the selected program open. The Running
Tools area of the Ghidra Project Window now shows the newly launched tool.


![](images/FrontEndWithProgram.png)


Alternatively, programs can be dropped onto running tools (either the icon in
the Running Tools area or onto the tool itself). In this case, the program is opened in the
existing tool in addition to any programs that are already open.


## Opening a Versioned Program File


If you attempt to open a versioned program file that is not checked out, a
dialog is displayed to warn you of this. You will not be allowed to save changes to this file
unless you check it out.


![](images/FileNotCheckedOut.png)


If you are working in a [shared project](../VersionControl/project_repository.md), AND if you plan to make
drastic changes to memory, e.g., add or remove memory blocks, select the checkbox on the
dialog to obtain an [exclusive lock](../VersionControl/project_repository.md#exclusivelock) on the
program file.


If you choose the "No" option, the program will be opened *read only*,
thus you will have to save your changes to *another* filename.


*Provided by: *ProgramManagerPlugin**


**Related Topics:**


- [Ghidra Programs](../Program/Ghidra_Programs.md)
- [Importing Programs](../ImporterPlugin/importer.md)
- [Closing Programs](Closing_Program_Files.md)
- [Shared Project](../VersionControl/project_repository.md)


---

[← Previous: Export Program](../ExporterPlugin/exporter.md) | [Next: Close Program →](Closing_Program_Files.md)
