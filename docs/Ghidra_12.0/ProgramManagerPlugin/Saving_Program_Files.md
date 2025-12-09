[Home](../index.md) > [ProgramManagerPlugin](index.md) > Save Program

# Saving Program


When changes are made to a program, the user must save the program.  Otherwise, those
changes will be lost.  The user can either save the changed program back to the original
program file or save the changed program to a new file, leaving the original program file
unchanged.


## Save


Saves the changed program back to the original program file. The **Save** option is only
enabled when changes have been made. To perform this action:


1. From the Ghidra Tool's menu, select **File →  Save**.


or


Select the Save icon ![disk.png](../icons/disk.png) in
the tool bar at the top of the Ghidra Tool.


## Save As


Saves the currently open program to a new program file. This new program file becomes the
program that is active in the tool.  When selecting **Save As...**, Ghidra will prompt
for a filename. To perform this action:


1. From the Ghidra Tool's menu, select **File →  Save As...**.
2. The *Save As...* dialog appears.


![](images/SaveProgramAs.png)


1. Select the folder for saving the program and enter the new *Name* of the
program.
2. Click the **Save** button.
3. The program is saved to the new name. This new program is the one now active in the
Tool.


If an existing program is selected from the **Save As...** dialog, an
overwrite confirmation dialog will be displayed.


## Save All


Saves any currently open programs. If any program has never been saved before, Ghidra will
prompt for a filename.


1. From the Ghidra Tool's menu, select **File →  Save All**.


*Provided by: *Program Manager* Plugin*


**Related Topics:**


- [Open Program](Opening_Program_Files.md)
- [Close Program](Closing_Program_Files.md)


---

[← Previous: Rename Program](../FrontEndPlugin/Ghidra_Front_end.md) | [Next: Delete Program →](../FrontEndPlugin/Ghidra_Front_end.md)
