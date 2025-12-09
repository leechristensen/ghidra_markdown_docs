[Home](../index.md) > [VersionControl](index.md) > Project Repository

# Project Repository


Ghidra supports the concept of a *project repository* such that files in the repository
can be *versioned*.  Versioning allows you to track file
changes over the life of the project.  The repository supports check out, check in,
version history, and viewing what is checked out. When you check in your file, a new version is
created. The project repository can be used with or without a [Ghidra Server](../GhidraServer/GhidraServer.md). If the project is associated
with a Ghidra Server, the project is *shared*, meaning that
the *files in the project* are accessible by multiple users concurrently. The [Project Access
List](../FrontEndPlugin/Ghidra_Front_end.md#edit-project-access-list) defines which users are allowed to access the shared repository.  When you [create a new project](../FrontEndPlugin/Creating_a_Project.md), you can
specify whether it should be associated with a Ghidra Server.


For projects that are not shared, all files and versions are managed locally in your project
directory. For the shared project repository, files are maintained on the Ghidra Server. When
you check out a file, a file is created locally in your project directory. When you check in a
file, it is [merged](../Repository/Merge_Program_Files.md) (if necessary)
with the latest version to create a new version. Merging is necessary only for shared project
repositories, as with a non-shared project, the version you checked out is always the latest
version.


## Connect to the Server


When you open or view a shared project, Ghidra attempts to connect to the corresponding server.
Depending on which user authentication mode the server is using, you may have to enter a password.
If you choose not to connect or lose the connection to the repository server after opening
or viewing a project, shared files not
checked out will not be shown within the Ghidra Project Window, as they are unavailable for use.
Local project private files are not affected by the repository server connection and will always
be shown.  If you subsequently connect to the repository server, Ghidra will refresh
the project views to reflect the current state.


> **Tip:** The root folder node of the Project Data Tree view of a shared project will convey the
current connection status with green (connected) or red (disconnected) indicator.


If applicable, and
not currently connected to the shared repository server, a manual connection may be re-attempted by
clicking the **Connect Shared Repository** popup action on the root node of a shared project.
For the active project there is also a Connect status button in the lower-right corner of the
project window.  When this button shows the disconnected state
![disconnected.gif](../icons/disconnected.gif) it may be clicked to attempt a connection.
This may also be done from the *[Project
Info](../FrontEndPlugin/Project_Info.md)* dialog. When the active project repository connection is successful, the connection
status button changes to ![connected.gif](../icons/connected.gif).


> **Tip:** Successfully connecting to a Ghidra Server which corresponds to multiple named repositories will cause
all associated viewed projects within Ghidra to become connected or automatically connect
when subsequently opened.


### Troubleshooting a Failed Connection


If you fail to connect to the Ghidra Server, check the following:


- Verify that the client machine can "ping" the server machine.
- Verify that you are attempting to login using the correct authentication mode.
- Verify that the Ghidra Server administrator has added you as a user on the
server.
- If the server is using Ghidra Password authentication, you may need to have your
password reset to "changeme" by the Ghidra Server
administrator.
- Verify the host name and port of the Ghidra Server.
- Verify that the Ghidra Server is running: from a command window,
type


telnet [host] [port]


If the server is not listening on that port, you will get a failed connection message
from telnet.


## Version Control


Except for [merging](../Repository/Merge_Program_Files.md), accessing
version control features is the same regardless of whether your project repository is
shared.


### Add to Version Control


Add a file (or multiple files at once) to version control by selecting the file in the
Ghidra Project Window. You can either click on the tool bar icon, ![vcAdd.png](../icons/vcAdd.png), or right mouse click and choose the **Add to Version
Control...** option. A dialog is displayed so that you can add comments about the
file.


![](images/AddToVersionControlDialog.png)


Leave the checkbox selected for *Keep File Checked Out* so that you do not have
check out the file after you have added it to version control. This checkbox will be
selected and disabled automatically if you have the file open. The **Apply to All**
button allows you to associate the same comment for multiple files that you are adding to
version control. After you add the file, the Ghidra Project Window indicates the file's
check out state and version.


![](images/CheckedOut.png)


This image shows that the file
"Program_A" is associated with a shared project (note the blue border on the [file icon](../FrontEndPlugin/Ghidra_Front_end.md#fileicons)), and you
are now working with version 1 of 1.  The file "Program_B"
has not been added to version control (note the plain icon and no version information). It
is considered to be a "private" file. Private files are never visible to other users.


> **Tip:** A normal checkout is indicated by a
checkmark with a green background , while an
exclusive checkout is indicated by checkmark with a blue background . A checkmark with a red background indicates that a newer version has been checked-in
by another user.


> **Note:** A tool tip on the file (let the mouse pointer hover over it) shows the date
the file was checked out, and the date that is was last modified. An asterisk will appear
on the file icon to indicate that changes have been made but not checked in.


### Check Out


To check out a file, select the file in the Ghidra Project Window. You can either
click on the check out icon ![vcCheckOut.png](../icons/vcCheckOut.png) on the tool
bar, or right mouse click on the file and choose the **Check Out...**
option.


![](images/CheckOutFile.png)


If your project repository is shared, a dialog is displayed to allow you to request an
***exclusive lock*** on the file.  An exclusive
lock is necessary if you plan to [manipulate the memory map](../MemoryMapPlugin/Memory_Map.md) in any way,
e.g., move or delete memory blocks, [change the program's
language](../LanguageProviderPlugin/Languages.md#set-language), etc. An exclusive lock can be granted if no other user has the file checked
out. While the exclusive lock exists, no other user can check out the file.


> **Note:** The exclusive lock is implied for a non-shared project repository.


### Check In


After you have made your changes and saved them, you are ready to check in your file.
(You cannot check in a file that was not changed.) The check in creates a new version for
this file. To check in the file, select the file in the Ghidra Project Window. You can
either click on the check in icon ![vcCheckIn.png](../icons/vcCheckIn.png) on the
tool bar, or right mouse click and select the **Check In...** option.


A dialog is displayed so that you can enter comments that describe your changes.


> **Tip:** The toolbar action icon is also
available from within the tool where you have the file opened.


![](images/CheckInFile.png)


The checkbox for *Keep File Checked Out* is selected and disabled automatically if
you still have the file open. If the file is closed and you plan to create more versions,
leave the checkbox selected for *Keep File Checked Out*. The checkbox for *Create
".keep" file* is selected by default; this option causes a copy of the file that you are
checking in to be created on your local file system.


In a shared project repository, when you check in your file, the changes in your file
may have to be [merged](../Repository/Merge_Program_Files.md) into the
latest version on the server.  This will be the case if another user checks in a file
since you did a checkout on the file. Under most conditions, the merge will be automatic
without any intervention required on your part. However, if you made changes such that a
conflict arises, you will have to [resolve the conflict](../Repository/Merge_Program_Files.md#resolveconflicts)
at the time of check in. When another user checks in his file, you will see [navigation markers](../CodeBrowserPlugin/CodeBrowser.md#cbnavigationmarkers)
for changes made since you checked out your file.  Potential conflicts are indicated
in red. Refer to the [Merge](../Repository/Merge_Program_Files.md)
page for more information about merging.


### Undo Checkout


You may want to undo your checkout such that you lose all your changes, and your file
reverts to the latest version on the server.


To undo a checkout:


1. Close the checked out file.
2. Select the checked out file in the Ghidra Project Window.
3. You can either click on the undo checkout icon ![vcUndoCheckOut.png](../icons/vcUndoCheckOut.png) in the tool bar, or right mouse click on the
selected file and choose the **Undo Checkout** option. If you had made changes to the
file, a dialog is displayed confirm the undo check out.


![](images/UndoCheckoutDialog.png)


If the checkbox on the dialog is selected, then a private file is created
with a ".keep" extension on the filename. The checkbox is selected by default.


![](../shared/note.yellow.png)


> **Note:** When a file is checked-out a copy of the file and
its folder path is created within the private project data store.  When an undo checkout
is performed that file and any empty parent folders are removed from the private data
store.  This is done to ensure any folder name changes or removals within a shared project
repository are properly reflected while connected and avoid showing old/stale folders.


### Update


While you are working on a program in a shared project repository, you may want to
periodically update your program to receive any changes made by others who are working in
the same shared project repository.  Use the **Update...** option to bring your
copy into sync with the latest version of the program in the repository.  If your
changes conflict with those made in the latest version, you will be prompted to [merge](../Repository/Merge_Program_Files.md) changes from the latest version
into your program.


Consider this scenario:  Suppose you are working on version 4 of 5 of a
program.  The "5" indicates that there are 5 versions of the program in the
repository.  The "4" indicates that your working copy of the program is based on the
version "4" version that you checked out from the repository.  (To see the version
numbers for your programs, check the [file's status](../FrontEndPlugin/Ghidra_Front_end.md#versionstatus) in the
Ghidra Project Window [data tree](../FrontEndPlugin/Ghidra_Front_end.md#datatree)).   When
you update, you will update to the latest version in the repository (5).  After the
update is complete, your file status will show "Version 5 of 5" just as though you had
*checked out* version 5. The **Update...** option allows you to have the latest
changes applied to your program without your having to check in your file.


To update your current program either select the program in the Ghidra Project Window
and click on the update icon ![vcMerge.png](../icons/vcMerge.png) in the tool
bar, or right mouse click and choose the **Update...** option.   The Update
option is only enabled when the latest version number on the server is **greater** than
the version that you checked out.


> **Tip:** The icon is also available from the
tool where you have the file opened.


> **Note:** The update action is not applicable in a non-shared project repository.


### Undo Hijack


A file becomes "hijacked" when it exists locally as a private file in your project
*and* a file of the same name exists in the repository.  This will happen when
user another adds a file to version control while you have a private file of the same name
in your shared project. It can also happen if your checkout of the file is [terminated](#terminatecheckout).  The [file icon](../FrontEndPlugin/Ghidra_Front_end.md#hijackedfile) in the Ghidra
Project Window changes to indicate that it is hijacked. To undo the hijack:


1. Close the file if you have it open.
2. Right mouse click on the hijacked file(s) in the Ghidra Project Window .
3. Select **Undo Hijack...**. The following dialog is displayed to confirm the undo
hijack.


![](images/UndoHijack.png)


Deselect the checkbox next to the name if you do not want to undo the
hijack for that file. The checkbox, *Save copy of the file with a .keep extension*, is
selected by default; if the checkbox is selected, a .keep file will be created. In this
example, you would see **SharedProgram.exe.keep** in your project data tree after you
select the **OK** button.  The checkbox selection applies to all the files that you
have selected for the undo hijack.


## Show Version History


To show the history on any versioned file, right mouse click on the file in the Ghidra
Project Window, and select the **Show History...** option. The table shows the date on
which the version was created, the user that created it, and the comments describing the
version.


![](images/VersionHistory.png)


### View Version


To view any version in the history, select the version, right mouse click and choose the
**Open With** → `<tool>` where
`<tool>` denotes a menu item for each tool in your tool chest. The version is read only
and is opened in the selected tool. The filename shown in the title of the tool indicates
the version number, e.g., "SharedProgram.exe@10 [Read Only]" indicates you are viewing
version 10 of SharedProgram.exe.  You can make changes to the file, but you must save
it to a new name.


> **Tip:** Other ways to open a specific version in a tool are:


- Drag a version from the *Version History* dialog to a running tool, the running
tool's icon, or to a tool icon in the tool chest.
- If you have a [default tool](../Tool/Ghidra_Tool_Administration.md#set-tool-associations)
specified, double click on the version that you want to open.
- Choose the **File** → **Open...** option; the [Open Program
dialog](../ProgramManagerPlugin/Opening_Program_Files.md#versionhistory) is displayed; from this dialog you can select a version to
open.


### Delete


You can delete the first and last version if you are the owner, or if you are an [administrator](../FrontEndPlugin/Creating_a_Project.md#admin) in the
project, *and* if the file is not checked out.  If the user who has the file
checked out is not available to either undo his checkout or check in his file, the
administrator may [terminate the checkout](#terminatecheckout) in order to
delete the version.


## View Checkouts


To view a list of who has a file checked out, right mouse click on the file in the Ghidra
Project Window, and select the **View Checkouts...** option.


![](images/ViewCheckouts.png)


The *Checkout Date* is when you checked out the file; the *Version* is the
version number of the file that you have checked out.


If you have administrative privileges in the project repository, you can terminate the
checkout. Right mouse click on the version and choose the **Terminate Checkout** option. A dialog is displayed to confirm the
terminate checkout action. The administrator may need to do this if users who have files
checked out are no longer working on the project. If your checkout is terminated, the file
becomes [hijacked](../FrontEndPlugin/Ghidra_Front_end.md#hijackedfile).


## Find Checkouts


To view a list of all the files that you have checked out in a folder and all of its
subfolders, select a folder, right mouse click and choose **Find Checkouts...**. In the
sample image below, all checkouts from the root project directory (pathname of "/") are
displayed; one file from the "TestFiles" folder is checked out.


![](images/FindMyCheckouts.png)


*Name* is the name of the file;. *Pathname* is the complete path to
the file. *Checkout Date* is when you checked out the file.  *Version* is the
version number of the file that you have checked out.


From this dialog, you can
[check in](#check-in) your files or [undo your
checkout](#undocheckout). Make a selection in the table, right mouse click and choose **Check In...**
or **Undo Checkout**. You can also click on the toolbar icon ![vcCheckIn.png](../icons/vcCheckIn.png)  to check in, or click on the icon ![vcUndoCheckOut.png](../icons/vcUndoCheckOut.png)  to undo the check out.


**Related Topics:**


- [Ghidra
Server](../GhidraServer/GhidraServer.md)
- [Creating a Shared
Project](../FrontEndPlugin/Creating_a_Project.md#createsharedproject)
- [Merging
Program Files](../Repository/Merge_Program_Files.md)
- [Open a
Version](../ProgramManagerPlugin/Opening_Program_Files.md#versionhistory)
- [Ghidra File Status](../FrontEndPlugin/Ghidra_Front_end.md#fileicons)
- [Project
Information](../FrontEndPlugin/Project_Info.md)


---

[← Previous: Restore Project](../FrontEndPlugin/Restore_Project.md) | [Next: Project Access List →](../FrontEndPlugin/Ghidra_Front_end.md)
