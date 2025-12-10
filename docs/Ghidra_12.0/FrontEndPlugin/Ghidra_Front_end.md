[Home](../index.md) > [FrontEndPlugin](index.md) > Delete Program

# Ghidra Project Window


The Project Window is displayed when you run Ghidra. From this window, you manage your [projects](../Project/Ghidra_Projects.md), [workspaces](#workspaces), [Programs](../Program/Ghidra_Programs.md),  and [tools](../Tool/Ghidra_Tool_Administration.md). If you are running Ghidra for
the first time, you will need to create a [new project](Creating_a_Project.md) to
get started.


The Project Window is a tool and may be [configured](Ghidra_Front_end_Menus.md#configure-project-window) with "special" [plugins](../Tool/Ghidra_Tool_Administration.md#plugins) that provide general
capabilities that may be required at a high level. By default, the Project Window contains
plugins for [importing](../ImporterPlugin/importer.md) and [exporting Programs](../ExporterPlugin/exporter.md),
[archiving a project](Archive_Project.md), and [restoring an archived project](Restore_Project.md). These plugins may be added to other
tools.


> **Note:** The options for archiving
and restoring a project will show up only in the Ghidra Project window, even though the plugins
providing these options can be added to other tools.


![](images/ProjectWindow.png)


The following sections describe the Project Window:


- [Tool Chest](#tool-chest)
- [Active Project Panel](#active-project)
- [Read-Only Project Data Panel](#read-only-project-data)
- [Workspaces](#workspaces)
- [Running Tools](#running-tools)
- [Project Repository](../VersionControl/project_repository.md)
- [Ghidra Server Connection Status](#ghidra-server-connection-status)
- [Data Tree](#project-data-tree)
- [Data Table](#project-data-table)
- [File Icons](#file-icons)
- [Ghidra URL Formats](#ghidra-url-formats)
- [Console](#console)
- [Configure Project Window](Ghidra_Front_end_Menus.md#configure-project-window)
- [Edit Menu Options](Ghidra_Front_end_Menus.md#edit-menu-options)
- [Manage Tools](../Tool/Ghidra_Tool_Administration.md)
- [Getting Help](#getting-help)
- [Exit Ghidra](Ghidra_Front_end_Menus.md#exiting-ghidra)


## Tool Chest


The Tool Chest shows the tools that you currently have in your
**`<user settings>`/tools** folder.
The tools are placed there when you initially install Ghidra.
These tools are always available to your currently open project. See [Ghidra Tool Administration](../Tool/Ghidra_Tool_Administration.md) for
information on managing tools. The Tool Chest panel is a tool bar with an icon that
represents each tool in your Tool Chest.


You can launch a tool by clicking on the icon. You can launch a tool with a Program by
dragging a Program file from the [Project data tree](#project-data-tree) and
dropping it on the tool icon in the Tool Chest.


## Active Project


The Active Project view shows the various files associated with the current
project which has been open for update.  Project files generally consist of programs and
datatype archives but may also be related to other Ghidra content.
The tree view is useful for organizing your files into folders and sub-folders.
The table view is useful for sorting all your files on some particular attribute such as
size, processor, or modification date.  In either view, you open and perform various
actions on program files or datatype archives.


### Project Data Tree


![](images/ProjectDataTree.png)


The data tree shows all files in the project orgnanized into folders and sub-folders.
[Icons for files](#file-icons) indicate whether they are under [version control](../VersionControl/project_repository.md#versioning) and whether
you have the file [checked out](../VersionControl/project_repository.md#samplecheckouticon).
In addition, unique icons are used to reflect content-type and if it corresponds to
a link-file referring to another file or folder (see [creating links](#paste-copied-folder-or-file-as-a-link)).
Open this view by activating the project window "Tree View" tab.  Within the tree view
internally linked-folders may be expanded to reveal the linked content which corresponds
to another folder within the project.


> **Tip:** Although Ghidra allows a folder and file within
the same parent folder to have the same name, it is recommended this be avoided if possible.
Allowing both a folder and file to have the same pathname can result in ambiguous path problems
when using link files and/or Ghidra URLs where only a path is used to identify either a project
resource.


### Tree Only Actions


The
data tree supports the following operations:


#### Create New Folder


To create a new folder,


1. Select a folder which should contain the new folder.
2. Right mouse click and choose the *New Folder* option.
3. A new node is created in the tree; a cell editor is displayed, containing the
default name, New Folder; enter a new name, or the `<Escape>` key to cancel the
editing.


#### Copy Folders and Files


To copy folders and files to another folder that you own,


1. Select a file or folder; you may also select multiple folders and files.
> **Note:** If you select a
folder, then any selections that are descendants of this folder are ignored.
2. Right mouse click and choose the  *Copy* option.
3. Select a destination folder.
4. Right mouse click and choose the *Paste* option. For very large files, an "in
progress" dialog is displayed. You may cancel the paste operation at any
time.


#### Paste Copied Folder or File as a Link


A Link may be created within the active project to a file or folder within the
same project (internal) or to a viewed project/repository (external).
Internal links may be defined using either a relative path or an absolute path.  Once
a link is created its stored path will not change.  The link will need to be replaced
should the referenced path need to be changed.  In addition, file-links are specific
to the content-type of the referenced file at the time of link creation (e.g.,
ProgramLink).


To create a Link use the following steps from the source project data tree:


1. Select a single file or folder, right mouse click and choose the  *Copy* option.
2. Select a destination folder within the active project data tree.
3. Right mouse click and choose the *Paste as Link* or *Paste as Relative-Link*
option.


See [Create Linked Folder or File](#create-linked-folder-or-file) for more information
about links and creating external links.


An internal link in the project tree may indicate a "broken" status for
various reasons, including:


- The referenced file or folder does not exist,
- the content-type at the referenced location does not match the link type, or
- a folder-link results in a circular path reference.


A broken link will have an icon which conveys its type but with a jagged red line
through it and a tooltip which conveys the issue detected.


> **Note:** External links will never show a broken
link state since they are not evaluated for such conditions.


#### Move Folders and Files


To move folders and files to another folder that you own,


1. Select a file or folder; you may also select multiple folders and files.
> **Note:** If you select a
folder, then any selections that are descendants of this folder are ignored.
2. Right mouse click and choose the *Cut* option; the icon will change to a
dithered image to indicate the cut operation.
3. Select a destination folder.
4. Right mouse click and choose the *Paste* option.


> **Note:** You cannot move a
file that is in use or a folder that contains a file that is in use.


#### Drag/Drop for Copy


You can get the same effect of Copy/Paste using Drag and Drop.


1. Select a folder or file (or multiple folders and files).
2. Hold the Ctrl key down and drag the object to another folder.
3. Drop the object on a folder.


> **Note:** You will not get a
valid drop target for folders that you do not own.


> **Note:** If you release the
Ctrl key during the drag, the operation changes to a move if you are dragging from
a folder that you own. Dragging files from another user always results in a copy ,
regardless of whether you hold down the Ctrl key.


#### Drag/Drop for Move


You can get the same effect of Cut/Paste using Drag and Drop.


1. Select a folder or file and drag it to a folder that you own.
2. Release the mouse button when you get a valid drop target.


> **Note:** You cannot move a
file that is in use or a folder that contains a file that is in use.


> **Note:** If a folder or file
already exists in the destination folder, Ghidra will append a ".copy" to the name to make
it unique.


#### Expand/Collapse


To expand a folder and all of its descendant folders,


1. Select a folder.
2. Right mouse click and choose the **Expand All** option.


To collapse a folder and all of its descendant folders,


1. Select a folder.
2. Right mouse click and choose the **Collapse All** option.


#### Follow Link


Select the internal or external folder or file referenced by a selected link-file.
While internal folders may be expanded directly from a folder-link, following a link
to the actual referenced location may be useful at times.


1. Select a file-link or folder-link, right mouse click and choose the *Follow Link*
option.  The referenced file or folder will be selected if possible.  If associated
with an external project or repository the selection will occur in a READ-ONLY
project view once opened.


#### Select Real File or Folder


Select a folder or file tree node from an expanded linked-folder or sub-folder
node.  Content is considered linked if one of its parent nodes corresponds to an
expanded folder-link. This linked-content corresponds to a real file or folder
contained within another folder.  The ability to select the real file or folder
may be useful when trying to understand the true origin of such content since this
path is not displayed.


1. Select a folder or file tree node from an expanded linked-folder or linked-sub-folder
node, right mouse click and choose the *Select Real File* or *Select Real Folder*
option.  The real file or folder will be selected within the tree if possible.


### Project Data Table


![](images/ProjectDataTable.png)


The data table shows all files in the project in a table sorted by some attribute
of the file. In the example above, the files are sorted on file type.
[Icons for files](#file-icons)
indicate whether they are under [version control](../VersionControl/project_repository.md#versioning) and whether
you have the file [checked out](../VersionControl/project_repository.md#samplecheckouticon).
To open this view, active the "Table View" tab.


### Actions for Both the Data Tree and the Data Table


#### Delete


Deleting folders is a recursive operation, so all descendant folders and files are
also deleted. **This is a *permanent*
operation.**  To delete a folder or file,


1. Select the folder or file or select multiple folders and files.
> **Note:** If you select a
folder, then any selections that are descendants of this folder are ignored.
2. Right mouse click and choose the **Delete** option.


> **Note:** The Delete option
is disabled for a file that is in use.


#### Rename


To rename a folder or file,


1. Select the folder or file.
2. Right mouse click and choose the **Rename** option.
3. A cell editor is displayed; enter the new name.


Duplicate names are not allowed within the same folder.


> **Note:** You cannot rename a
file that is in use.


> **Note:** You cannot rename
your project folder.


#### Select All


To select a folder and all of its descendants,


1. Select a folder.
2. Right mouse click and choose the **Select All** option.


#### Read-Only


To mark a file as read only,


1. Select a file.
2. Right mouse click and choose the **Read-Only**
option.


The icon for the file is updated to indicate the read only state. When you right mouse
click, a check mark shows up in the Read-Only option.


> **Note:** A read-only
Program must be saved to a new name if you make changes to it.


> **Note:** You cannot change
the read-only state of a file while it is in use.


#### Drag File to a Tool


- To launch a tool with a specific file, drag a file to the tool icon in the Tool
Chest.
- To open a file in a *running tool*, drag a file to the tool icon in the [Running Tools](#running-tools) tool bar, OR drag the file to the tool window.


#### Open a File in the Default Tool


- To open a file in the tool that was [specified as the
"default,"](../Tool/Ghidra_Tool_Administration.md#set-tool-associations) double click on the Program that you want to open, OR right mouse click on
the file and choose **Open in Default Tool.**  Either a new tool will be launched
or an existing running tool will be reused based upon the Tool option setting (see
[Front-End Tool Options](../Tool/ToolOptions_Dialog.md#tool).


#### Open a File With a Specific Tool


- To launch a tool with a specific file,


1. Select the file.
2. Right mouse click and choose **Open With** → &lt;***tool*** ***name***&gt;.


#### Refresh


The ![Refresh](../icons/reload3.png) button on the
tool bar refreshes the list of files in the selected folders. This is a way to sync the
project folder/file structure with the project repository. The list of files and folders
in the Project Data Tree is updated. This button is enabled only for selected folders.
You can also refresh folders from a [viewed project](#view-other-projects) or
[viewed repository](#view-a-repository).


#### About


To [view information about a
file](../About/About_Program_File.md), right mouse click on the file in the data tree and choose the **About Program**
option.


### Version Control Actions


There are numerous actions related to version control.  See [Project Repository](../VersionControl/project_repository.md)
for details.





### File Icons


The Project Data Tree shows icons for the following types of files:


| ![program_obj.png](../icons/program_obj.png) | -   | [Program](../Program/Ghidra_Programs.md)   |
| --- | --- | --- |
| ![closedBookBlue.png](../icons/closedBookBlue.png) | -   | [Data Type Archive](../DataTypeManagerPlugin/data_type_manager_description.md#project-data-type-archive) (a data type file             stored in the project)   |
| ![video-x-generic16.png](../icons/video-x-generic16.png) | -   | Debugger Trace Data   |
| ![start-here_16.png](../icons/start-here_16.png) | -   | Version Tracking Session Data   |


The Project Data Tree shows modifications to these icons for
files in the following states:


| File Status | Sample Icon | Description |
| --- | --- | --- |
| [Versioned File](../VersionControl/project_repository.md#version-control) not               checked out. | ![](images/VersionedFileIcon.png) | The program named "Example" is versioned as indicated by                the light purple background. It is not checked out , since there is no circle with a                check mark. Version 1 is the latest version, as indicated by "(1)";                 the version will be the latest version when the file is not checked out. |
| Versioned File is [Checked out](../VersionControl/project_repository.md#check-out) exclusively                by you. | ![](images/VersionedFileCOnoServer.png) | Version 1 of the program named "Example" is checked out, as indicated                by "(1 of 1)"; Version 1 is the latest version. The blue check mark icon indicates                that the file is checked out with an [exclusive](../VersionControl/project_repository.md#exclusivelock) lock.   If your project is not associated with a Ghidra Server,                you will always have the latest version checked out and the check out will always                be exclusive,  since the project is not shared. |
| Versioned File is Checked Out; the project is associated with a               Ghidra Server | ![](images/VersionedFileCOwithServer.png) | Version 3 of the program named "Example" is checked out; Version 3 is the latest               version on the server, as indicated by "(3 of 3)" and the green circle with a                check mark. The asterisk indicates you have changes to the file which have not been                checked in yet. |
| Versioned File is Checked Out; the project is associated with a               Ghidra Server. A newer version exists on the server. | ![](images/CheckedOutNotLatest.png) | Version 2 of the program named "Example" is checked out; a Version 3               has been created since Version 2 was checked out, as indicated by "(2 of 3)" and               the magenta circle with a check mark. The asterisk indicates you have changes to the                file which have not been checked in yet. |
| Private File | ![](images/PrivateFileIcon.png) | A program named "Example" is               not under version control, exists only on your local machine, and is not visible to               other users. |
| File Link | ![](images/AbsoluteFileLinkIcon.png) | A file link named "Example" which refers to               a Program at */data/example* .   File links may reference another file using either an               1) absolute file path within the same project, 2) a relative file path within               the same project, 3) a shared repository Ghidra URL, or 4) a local project Ghidra URL.               See [Ghidra URL formats](#ghidra-url-formats) below.               A file link may appear with various icon states which correspond to version control.               File links only support a single version and may not be modified. |
| File Link (Broken) | ![](images/AbsoluteBrokenFileLinkIcon.png) | A file link named "Example" which refers to               a Program at */data/example* and is in a "Broken" state.  Hovering the mouse 			  on this node will display a tooltip which indicates the reason for the broken state.  			  External file links will never show a broken link state since they are not evaluated for such conditions. |
| Folder Link | ![](images/AbsoluteFolderLinkIcon.png) | A folder link named "Example" which refers               to a folder at */data/example* .   Folder links may reference another folder using either an               1) absolute file path within the same project, 2) a relative file path within               the same project, 3) a shared repository Ghidra URL, or 4) a local project Ghidra URL.               See [Ghidra URL formats](#ghidra-url-formats) below.               Since a folder link is stored as a file, it may appear with various icon states which                correspond to version control.  Folder links only support a single version and may not                be modified.  The tree may permit expanding such nodes to reveal their linked-content  			  as files and sub-folders. |
| Folder Link (Broken) | ![](images/AbsoluteBrokenFolderLinkIcon.png) | A folder link named "Example" which refers to               a folder at */data/example* and is in a "Broken" state.  Hovering the mouse 			  on this node will display a tooltip which indicates the reason for the broken state.   			  External folder links will never show a broken link state since they are not evaluated for such conditions. |
| Hijacked File | ![](images/hijack_file.png) | The private file "Example" exists on your                computer, but another user added "Example" to version control, which               caused the private file to appear as *hijacked* , (i.e., the file can be saved "as               is" using " **Save As** " since you do not have the file checked out that is on                the Ghidra Server.) Hijacked files may also result from a checkout that was [terminated](../VersionControl/project_repository.md#terminatecheckout) . The *shared* version of "Example" will not be visible in your project until you [undo the               hijack](../VersionControl/project_repository.md#undo-hijack) .  You can also either rename the hijacked "Example", move it to               another folder, delete it, or use the **Undo Hijack** [action](../VersionControl/project_repository.md#undo-hijack) . Then the               shared "Example" will appear in your data tree as a versioned file. |


### Ghidra URL Formats


The format of a remote *Ghidra Server URL* is distinctly different from a
*Local Ghidra Project URL*. These URLs have the following formats:


**Remote Ghidra Server Repository**


| `ghidra://<hostname>[:<port>]/<repository_name>[/<folder_or_file_path>]` |
| --- |


If the default Ghidra Server port (13100) is in use it is not specified by the URL.
The *hostname* may specify either a Fully Qualified Domain Name (FQDN, e.g.,
*host.abc.com*) or IP v4 Address (e.g., *1.2.3.4*).


**Local Ghidra Project**


| `ghidra:[/<directory_path>]/<project_name>[?/<folder_or_file_path>]` |
| --- |


For local project URLs, the absolute directory path containing the project
**.gpr* locator file is specified with the project name but excludes any *.gpr/.rep* suffix.
The folder or file path within the project is conveyed with a URL query so the '?' is required.


## Read-Only Project Data


You can view data from other Projects or remote Repositories and copy data into your current
Project's data folders.


### View Other Projects


To view the data from another project:


1. Select **Project →
View Project...**
2. A file chooser is displayed; the default location is the projects folder in the
installation folder.
3. Choose a project; the file extension is "gpr."
4. A new tab for the data tree is created in the "READ-ONLY Project Data" panel in the
Project Window, next to the Active Project panel; the tab shows the name of the
project.
5. The list of [recent projects menu](#view-recent) is updated to include
this project.


| ![](images/ViewOtherProjects.png) |
| --- |


You can copy and paste folders (via menus or drag and drop) and files from the other
view to your folders.


> **Tip:** You do not have to
hold the Ctrl key down when you drag from the other view since this cannot be a move
operation, as this view is always read-only.


### View a Shared Project


You view a shared project the same way you would a non-shared project; the difference is
that when you view the shared project, an attempt is made to connect to the Ghidra Server
associated with that project. Depending on the user authentication mode of the Ghidra
Server for the other shared project, you may have to enter a password. If the connection to
the Ghidra Server is unsuccessful, then the only files available to you are your [private files](../VersionControl/project_repository.md#privatefile).


### View a Repository


To view the data from a server-based repository:


1. Select **Project →
View Repository...**
2. A repository chooser is displayed; allowing you to specify a Ghidra Server
network address and select one of its repositories...
3. Enter the Ghidra Server address and port.  The default port is 13100.
4. Click the Refresh button to the right of the host name and port fields.  This will
connect to the specified Ghidra Server and list available repositories for which
you have been granted access.  You may be prompted for a password should user authentication
be needed.
5. Select the desired repository from the list of those available.
6. Click the **Select Repository** button.  A new tab for the data tree is created
in the "READ-ONLY Project Data" panel in the
Project Window, next to the Active Project panel; the tab shows the URL of the
remote repository.
7. The list of [recent projects/repositories menu](#view-recent) is updated to include
this repository.


### View Recent


Ghidra maintains a list of Projects and remote Repositories that were recently viewed.


To view a recently opened project or repository,


1. Select **Project →
View Recent →
&lt;*project path or repository URL*&gt;**
2. Select a project or repository from the menu.
- If the project/repository is not in the view, a new tab is created in the "READ-ONLY Project
Data" panel in the Project Window; the tab shows the name of the project or repository URL.
- If the tab is in the view, then the tab for this project/repository is selected.


### Close View


To close a view, select **Project****→****Close View****→****&lt;*project path/repository URL*&gt;,**
OR click on the small 'X' on the specific view tab, OR right mouse click on the
corresponding view tab and choose the **Close**
option.


The tab is removed from the "READ-ONLY Project Data" panel in the Project Window.


### Close All Read-Only Views


To close all read-only views at once, select **Project****→****Close View****→****Close All Read-Only Views.**


The tabbed pane for read-only Project data is removed from the Project Window.


### Create Linked Folder or File


This feature allows you to create a folder or file link in your active project to a
corresponding folder or file within your project or to a read-only viewed project.
External links are established using a Ghidra URL which references a
file or folder in its local or remote storage location.  An external Ghidra URL will
be used if a link refers to a viewed project or repository.  It is possible for internal links to
become broken if the referenced file or folder location has changed (e.g., no longers exists
or has the wrong content type).  External links may become invalid for various reasons
but will not convey an issue until the link is used.  The broken link icon does not apply
to external link files.


To create an external folder or file link the following steps may be used:


1. Select a single folder or file from a viewed READ-ONLY Project Data tree.
2. Right mouse click on the selected tree node and choose the *Copy* option.
3. Select a destination folder in the active project data tree.
4. Right mouse click on the folder and choose the *Paste as Link* option.


It is important to note that the resulting link is always stored as a file within the
project.  With the exception of external links to local project content, a link may be
added to version control so that it may be shared.  Once added to version control it cannot
be checked-out, since they are immutable, however they can still be deleted.


A file-link may be opened in a tool via the project window in the same fashion that
a normal file is opened (e.g., double-left-mouse-click or drag-n-drop onto a tool box icon).
Such a project file may also be opened within a Tool using its **File-&gt;Open...** action
and selected from the resulting project file selection dilaog.
Clicking on an external folder-link in the active project window will open that location in a
**READ-ONLY Project Data** tree.  The user may be prompted for a shared repository
connection password when accessing an external folder or file link.


Within a project file chooser dialog a folder-link may be expanded in a similar fashion
to local folders provided any neccessary repository connection can be completed.


> **Note:** Currently, external file-links only provide access
to the latest file version and do not facilitate access to older file versions.  An external
folder-link will allow access to file versions contained within such a folder.


> **Note:** Some file chooser use cases, including the GhidraScript API, are restricted to selecting files and folders within the active
project only and will hide all external links.


The project window below shows a Program file-link "Program1" which is linked to the
same file in the viewed project.


![](images/LinkOtherProject.png)


A folder or file link will show its referenced location with either
same file in the viewed project.


## Workspaces


A workspace contains a set of [running tools](#running-tools), and the tools'
opened data. A workspace is analogous to a virtual desktop. When you switch to another
workspace, you switch to a different set of running tools. The tools from the other workspace
remain running, but are not visible until you switch back to that workspace.


The workspace names are listed in a combo box in the Running Tools panel. Switch to
another workspace by choosing a name from the list. The default workspace, named
"Workspace,"  is created in the project.


The workspace state, i.e., [running tools](#running-tools), [tool connections](Connecting_Tools.md), [tool configuration](../Tool/Configure_Tool.md), etc.,  is maintained when
you [exit Ghidra](Ghidra_Front_end_Menus.md#exiting-ghidra) or [close the Project](Close_Project.md).


- To create a new workspace,


1. Select **Project →
Workspace → Add...**
2. A dialog is displayed; enter a new workspace name. Duplicate workspace names are not
allowed.
3. Click on the **OK** button; the newly created workspace becomes
the current workspace; the name is added to the list of workspaces in the combo box.
> **Tip:** If you leave
"Workspace" as the new workspace name in the dialog and click on OK , a one-up
number is appended to the name to make it unique.


- To rename the current workspace,


1. Select **Project****→ Workspace → Rename...**
2. A dialog is displayed.
3. Enter the new name for the current workspace. Duplicate workspace names are not
allowed. The list of workspace names is updated to reflect the new name.


- To delete the current workspace,


1. Select **Project****→ Workspace → Delete...**
2. A dialog is displayed to confirm your delete request.
3. Choose the **Delete** button to delete the workspace.
- Tools in the workspace are closed.
- If you made changes to a file that is not open in any other tool, a dialog will be
displayed to prompt you to save your changes.
- The oldest workspace becomes the current workspace. If the deleted workspace was
the last one, then the default workspace ("Workspace") becomes the current
workspace.


- To switch workspaces,


1. Select **Project****→ Workspace → Switch...**
2. Switches sequentially through the list of workspaces (in creation order),
wrapping back to the first after the last has been reached.
3. If only 1 workspace exists, this action will do nothing.


### Running Tools


The Running Tools panel shows an icon for each tool that is running in the current
workspace. Click on the icon to bring that tool forward on your console. To close the tool
from the Running Tools panel, right mouse click on the icon for the tool and choose the
**Close** option.


To [connect running tools](Connecting_Tools.md#automatic-tool-connection),
drag one icon onto another icon. Those tools are connected for all [tool events](Connecting_Tools.md#toolevents).


> **Note:** Tools running in
different workspaces may be connected.


## Ghidra Server Connection Status


If your project is associated with a Ghidra Server, then below the *Running Tools*
panel you will see a connection status panel that shows the name of the [Project Repository](../VersionControl/project_repository.md), your access
privileges, and an indication of whether you are currently connected to the Ghidra
Server.  The [status button](../VersionControl/project_repository.md#connect-to-the-server), ![connected.gif](../icons/connected.gif) indicates that your
project repository is connected to the Ghidra Server; the status button, ![disconnected.gif](../icons/disconnected.gif) indicates that
your project repository is associated with a Ghidra Server but it is not connected to
it.


> **Note:** If your project is not
associated with a Ghidra Server, then this status panel is empty.


## Edit Project Access List


If your project is [shared](../VersionControl/project_repository.md#sharedproject), the Project menu
has an option to edit the [project access
list](Creating_a_Project.md#useraccesslist). This list controls what users have access to the project and what [privileges](Creating_a_Project.md#userprivileges) the users have. If you have
administrative privilege in the project, the option for **Project → Edit Project Access List** will
be enabled. The dialog displayed when you select this option shows a panel that is the same
as the one you see in the [New Project
Wizard](Creating_a_Project.md#creating-a-shared-project) when you set up the user list for new project. As in the New Project Wizard, this
dialog allows you to add and remove users, and change users' privileges in the project.


![](images/EditProjectAccessList.png)


> **Note:** In order for a user to
show up in the Known Users list, the server administrator must add a new user to the Ghidra Server.   This is accomplished
from a command shell on the server system using the svrAdmin command.  Refer to the server/svrREADME.html file in the installation
directory for use of this administration command.


> **Note:** If the user does not have administrative privilege in the project, the user will not be able to view
this full dialog and make edits. Instead, the option for Project View Project Access List will be enabled, which will display
the following dialog and allow the user to view the project users and their current access privileges only.


![](images/ViewProjectAccessPanel.png)


## Change Password


If your project is associated with a Ghidra Server that is using Ghidra password
authentication, then the menu item, **Project** → **Change Password...** will be present. Use this option when
you want to change your password. A dialog is displayed to confirm your request, as shown
below.


![](images/ConfirmChangePassword.png)


If you select **Continue**, a dialog is displayed for you to enter your
new password, and to re-enter your password.


![](images/ChangePassword.png)


> **Note:** When you initially
connect to the Ghidra Server using password authentication, your default password is " changeme ".  The default
password expires after 24 hours so you must change your password as soon as possible. If your
password expires or if a user forgets their password, the Ghidra Server administrator must reset your password.  This is accomplished from
a command shell on the server system using the svrAdmin command.  Refer to the server/svrREADME.html file in the installation
directory for use of this administration command.


## Console


Click on the console icon ![monitor.png](../icons/monitor.png)  to display the system console.


Log messages, including the standard output and error streams, are redirected to the
console. If you are running Ghidra in development mode (i.e., through Eclipse or some
other IDE),  you will see standard output and errors in your IDE's console as well as
the Ghidra console.


Errors and other informational messages are logged to a file in
`<user settings>`/***ghidraUser.log***.  Messages are appended to the file every
time you launch Ghidra.  Once the log file has reached 500KB in size, however, it will
be rolled to a backup file named ***ghidraUser.log.0***.  Older backup files are
similarly rolled to another file with a one-up digit suffix as well.  Ghidra stores a
maximum of three backup files (***ghidraUser.log.0***,
***ghidraUser.log.1***, ***ghidraUser.log.2***) at a time.  The log
files can be used by Ghidra developers for troubleshooting.


The field next to the icon in the Ghidra Project Window shows the last message sent to the
console (error messages are in red).


## Getting Help


### Context Sensitive Help


- Ghidra provides context sensitive help that pops up when you hit the &lt;**F1**&gt; or &lt;**Help**&gt;  key.


To get help on a menu option,


1. Display the menu (either from the tool menu or the popup) that has the option you
want help on.
2. Position the mouse pointer over the option.
3. Press the &lt;**F1**&gt; or &lt;**Help**&gt; key.
4. The Help Viewer is displayed and shows the appropriate help contents.


- To get help on a dialog or tool window, click somewhere in that window and press the
&lt;**F1**&gt; or &lt;**Help**&gt;
key.


If no specific help exists, then a [default page for Ghidra help](../Misc/Welcome_to_Ghidra_Help.md) is
displayed.


### About Ghidra


The [About Ghidra](../About/About_Ghidra.md) option shows build
information about the Ghidra application.


**Related Topics:**


- [Tool Administration](../Tool/Ghidra_Tool_Administration.md)
- [Projects](../Project/Ghidra_Projects.md)
- [Program](../Program/Ghidra_Programs.md)
- [Import Program](../ImporterPlugin/importer.md)
- [Export Program](../ExporterPlugin/exporter.md)
- [Welcome to Ghidra Help](../Misc/Welcome_to_Ghidra_Help.md)
- [Create a Shared Project](Creating_a_Project.md#creating-a-shared-project)
- [Project Repository](../VersionControl/project_repository.md)
- [Project Info dialog](Project_Info.md)


---

[← Previous: Save Program](../ProgramManagerPlugin/Saving_Program_Files.md) | [Next: About Program →](../About/About_Program_File.md)
