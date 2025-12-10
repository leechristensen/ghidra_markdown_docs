# Ghidra Front End Menus


## Configure Project Window


You can configure your [Project Window](Ghidra_Front_end.md)  just as you
would another tool, however, only a subset of the Ghidra [Plugins](../Tool/Ghidra_Tool_Administration.md#ghidra-tool-administration) will be included in the
list of available Plugins, as these Plugins are the only ones that may be added to the
Project Window. These Plugins are "marked" as providing general capabilities that may be
required at a high level, such as [importing
a Program](../ImporterPlugin/importer.md) into a Ghidra project, or [archiving](Archive_Project.md) the
active project. These "special" Plugins can also be added to any tool; however, the archive
and restore options show up only in the Ghidra Project Window even though the plugins
providing these options can be added to other tools. To bring up the *Configure Tool
Plugins*  dialog, select the **File** →
**Configure** option.


| ![](images/ConfigureTool.png) |
| --- |


The *Configure Tool* dialog shows a list of plugin packages that can be added to
the tool. Clicking the checkbox will add (or remove) all the plugins in the package to the
tool. Clicking on the **Configure** link will bring up a dialog for adding individual
plugins. See [Configure Tool](../Tool/Configure_Tool.md#configure-tool) for more information.


> **Note:** Adding or removing
Plugins may cause menu options to change.


> **Note:** The configuration for
your Project Window is saved when you save your
Project .


### Refresh


This action will refresh the list of available plugins, based upon what is found in the
[plugins path](Edit_Plugin_Path.md).


## **Edit** Menu Options


### Project Window and Tool Options


Each tool has an *[Options](../Tool/ToolOptions_Dialog.md)*
dialog to change [key
bindings](../Tool/ToolOptions_Dialog.md#key-bindings) and set [tool
options](../Tool/ToolOptions_Dialog.md#tool). In addition to these two option categories, the dialog has a node in the
Options tree for each category of options that are used by plugins in the tool. If a plugin
is removed from the tool, and no other plugin is using a set of options, then this category
will not be displayed the next time you run the tool and bring up the *Options*
dialog.


To bring up the *Options* dialog, select **Edit → Tool Options**


**Related Topics:**


- [Edit Plugin Path](Edit_Plugin_Path.md)
- [Key
Bindings](../Tool/ToolOptions_Dialog.md#key-bindings)


### PKI Certificate


The Ghidra Server can be set up to perform user authentication using PKI
certificates.  When the Ghidra Server is in this authentication mode, you must set
your PKI Certificate before you attempt to open a [project repository](../VersionControl/project_repository.md) or create a new [shared project](../VersionControl/project_repository.md#project-repository)
associated with this server.


To configure, choose **Edit → Set PKI Certificate...**. A
file chooser is displayed; select your PKI certificate file and select the **Set
Certificate** button. You must restart Ghidra in order for the setting to take effect.
When you connect to the server the next time you run Ghidra, you will be prompted for the
key-store password associated with this certificate key file. The path to your PKI
certificate file is saved as part of your Ghidra preferences.


> **Note:** If the Ghidra Server
is not using PKI Certificates for user authentication, you can ignore this menu option.


## Exiting Ghidra


To exit Ghidra,


- Select **File** →
**Exit Ghidra** option on the Project Window, OR


- Select  the native windowing system's window closing feature, OR


- Select **File** →
**Exit Ghidra** option from a running
tool.


> **Note:** If you have made
changes to read-only files, then the Read-Only Files dialog will appear.
It will indicate that you must do a Save As to
save these files to a new name. You can choose to Cancel and go perform the Save As or choose Lose Changes to continue without saving your changes
to the read-only file.


| ![](images/SaveReadOnly.png) |
| --- |


<a name="savedatadialog"></a>If you have made any changes to Programs, then a dialog is
displayed to prompt you to save changes. After the programs, all other files that have been
changed and not saved are listed.


| ![](images/SaveFiles.png) |
| --- |


By default, the check box is selected to do a save. You can select or deselect the check
boxes individually. Click on the buttons to either turn all the check boxes on (**Select All**) or off (**Select None**).


Your Ghidra preferences file is updated to record your last opened project. The position
of the Ghidra Project Window is also recorded so that when you run Ghidra again, the window
position is restored. If the Project configuration has changed (tools or
[workspaces](Ghidra_Front_end.md#workspaces) that were [added](../Tool/Ghidra_Tool_Administration.md#run-tool) or [removed](../Tool/Ghidra_Tool_Administration.md#close-tool), etc.),
the new configuration will be saved automatically.


**Related Topics:**


- [Ghidra Project Window](Ghidra_Front_end.md)
- [Project Repository](../VersionControl/project_repository.md)
- [Import Programs](../ImporterPlugin/importer.md)
- [Export Programs](../ExporterPlugin/exporter.md)
- [Archive Project](Archive_Project.md)
- [Restore Project](Restore_Project.md)
- [Tool Options Dialog](../Tool/ToolOptions_Dialog.md)
- [Plugins](../Tool/Ghidra_Tool_Administration.md#ghidra-tool-administration)
- [Configure Ghidra Tool](../Tool/Configure_Tool.md)
