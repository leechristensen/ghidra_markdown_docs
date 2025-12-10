[Home](../index.md) > [Project](index.md) > Ghidra Projects

# Ghidra Projects


A Ghidra project maintains information for a particular reverse engineering
(RE) effort. The RE effort involves using tools built with [plugins](../Tool/Ghidra_Tool_Administration.md#plugins)
to analyze target software. Tools are accessible across projects and not
associated with any one project in particular.  However,  the target
software is imported into a Ghidra project as [programs](../Program/Ghidra_Programs.md).
The Ghidra project organizes and
maintains these programs for multiple users.


The latest release of Ghidra introduces the concept of a [project
repository](../VersionControl/project_repository.md) that contains files that are [versioned](../VersionControl/project_repository.md#versioning),
shared, or private.  A shared project is associated with a Ghidra
Server that manages the files in the repository. Multiple users in the
project can add files, access files on the server and create new versions of the
files.  Private files are local your project and have not been added to a
project repository. You can still take advantage of the project repository
features and not have your project be associated with a Ghidra Server.


You can create subfolders and [import](../ImporterPlugin/importer.md) programs
into your project. You can also view other data from other projects, or drag the
other project data into your current project.


The [Ghidra Project Window](../FrontEndPlugin/Ghidra_Front_end.md)
shows the active project. The Ghidra Project Window's menu provides access
to the following project operations:


- [Create a project](../FrontEndPlugin/Creating_a_Project.md#creating-a-shared-project)
- [Open an existing project](../FrontEndPlugin/Opening_a_Ghidra_Project.md)
- [Close the project](../FrontEndPlugin/Close_Project.md)
- [Re-open a project](../FrontEndPlugin/Re-opening_a_Project.md#reopen-project)
- [View a recent project](../FrontEndPlugin/Ghidra_Front_end.md#view-recent)
- [Save the project](../FrontEndPlugin/Saving_a_Ghidra_Project.md)
- [Archive
the project](../FrontEndPlugin/Archive_Project.md)
- [Restore
an archived project](../FrontEndPlugin/Restore_Project.md)


**Related Topics:**


- [Ghidra Programs](../Program/Ghidra_Programs.md)
- [Ghidra Project Window](../FrontEndPlugin/Ghidra_Front_end.md)
- [Import Programs](../ImporterPlugin/importer.md)
- [Project Repository](../VersionControl/project_repository.md)


---

[← Previous: About Ghidra](../About/About_Ghidra.md) | [Next: New Project →](../FrontEndPlugin/Creating_a_Project.md)
