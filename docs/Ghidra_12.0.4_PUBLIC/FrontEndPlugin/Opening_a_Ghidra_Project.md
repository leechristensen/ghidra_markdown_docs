[Home](../index.md) > [FrontEndPlugin](index.md) > Open Project

# Open Project


When you open a Project, your active project is [closed](Close_Project.md); the
project identified in the *Open a Ghidra Project* dialog will be opened.  If the
active project has been modified since it was last saved, Ghidra will prompt you to save the
active project before closing it. The project window is restored with any [plugins](../Tool/Ghidra_Tool_Administration.md#ghidra-tool-administration) it had when you last
saved the project. Tools that were running when you last saved the project are launched;
programs that the tools had open are opened. The last active [workspace](Ghidra_Front_end.md#workspaces) from this project now shows up as the active
workspace. Other [viewed projects](Ghidra_Front_end.md#read-only-project-data)
are restored.


> **Note:** Projects that were
created using a release of Ghidra prior to 3.0 can be viewed only. You can drag the data from
the old project to your current project.


To open a project, choose it from a list of projects in the default project directory.
If the project has been opened before, then the project will appear in the [Reopen](Re-opening_a_Project.md) list.  If the project is being shared by others, it
may not reside in the default project directory.  Use the browse button, on the *Open a
Ghidra Project* dialog, to locate the target project.


To open a project:


1. From the Ghidra Project Window, select **File → Open Project...**. The *Open a Ghidra Project* dialog
appears.


![](images/OpenProject.png)


1. The dialog box filter defaults to *.gpr (project file extension). Select the project
from the *Open a Ghidra Project* dialog.


> **Note:** The project name can be
of any length.  The name of the project has the same restrictions that the operating
system imposes on file names.  A Ghidra Project name must have the .gpr extension.


1. Click the **Open Project** button. The selected project appears in the Ghidra Project
Window. If you are opening a [shared project](../VersionControl/project_repository.md#project-repository), Ghidra
attempts to [connect
to the Ghidra Server](../VersionControl/project_repository.md#connect-to-the-server). You may have to enter a password, depending on the type of
user authentication the Ghidra Server is using.


![](images/ProjectWindow.png)


If this were a shared project, the connection status button (![connected.gif](../icons/connected.gif)) would be displayed, indicating that the project was
successfully connected to the server. If the project failed to connect to the server, the
status button would appear as ![disconnected.gif](../icons/disconnected.gif).
If the server comes up after you have opened the shared project, you can click
on status button to attempt to connect to the server. You can still work offline in a shared
project, however, you will not be able to do any check outs or check ins.


**Related Topics:**


- [Ghidra Projects](../Project/Ghidra_Projects.md)
- [Close Project](Close_Project.md)
- [Save Project](Saving_a_Ghidra_Project.md)
- [Reopen Project](Re-opening_a_Project.md)
- [Archive Current Project](Archive_Project.md)


---

[← Previous: New Project](Creating_a_Project.md) | [Next: Close Project →](Close_Project.md)
