[Home](../index.md) > [FrontEndPlugin](index.md) > Reopen Project

# Reopen Project


Ghidra maintains a list of the projects that you recently opened. These are
available in the Ghidra Project Window's menu. Reopening a project will close any active
project and open the project selected from the Reopen menu. The project that was most recently
opened is placed first in the list.


![](images/ReopenProject.png)


To reopen a project:


- Select **File →
Reopen → *directory
path/project_name*** where ***directory_path/project_name*** indicates the project
from the list that you wish to reopen.


Ghidra will close any active project. It then opens ***project_name*** and restores
all of the project's configurations.


> **Note:** If the project that you
are re-opening is shared , then an attempt is
made to connect to the Ghidra Server. If the connection was not successful, you can still
access your private files and checked out files. Other files on the server will be
unavailable.


**Related Topics:**


- [Ghidra Projects](../Project/Ghidra_Projects.md)
- [Close Project](Close_Project.md)
- [Save Project](Saving_a_Ghidra_Project.md)
- [Open Project](Opening_a_Ghidra_Project.md)
- [Archive Current Project](Archive_Project.md)
- [Project Repository](../VersionControl/project_repository.md)


---

[← Previous: Close Project](Close_Project.md) | [Next: Save Project →](Saving_a_Ghidra_Project.md)
