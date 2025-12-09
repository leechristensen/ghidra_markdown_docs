# Ghidra Extensions


Ghidra Extensions are Ghidra software modules that can be installed
into a Ghidra distribution.  This allows users to create and share new plugins and scripts.
Ghidra ships with some pre-built extensions that not installed by default.


Ghidra Extensions can be installed and uninstalled at runtime, with the changes taking effect
when Ghidra is restarted. The extension installation dialog can
be opened by selecting the **Install Extensions** option on the project **File** menu.


| ![](images/ConfigureExtensions.png) |
| --- |


## Dialog Components


### Extensions Table


The list of extensions is populated when the dialog is launched. To build the list, Ghidra
looks in several locations:


- Extension Installation Directories: Contains any extensions that have been installed.
The directories are located at:
- - *[user settings]/Extensions* - Installed/uninstalled from
this dialog
- *[installation dir]/Ghidra/Extensions/* - Installed/uninstalled from
filesystem manually
- Extensions Archive Directory: This is where archive files (zips) that are bundled with
the distribution are stored. It is
located at *[installation dir]/Extensions/Ghidra/*.  This directory is not intended for
end-user extensions.


> **Tip:** The color red is used in the table
to indicate that the extension version does not match the Ghidra version.


**Note:** Extensions that have been installed directly into the Ghidra installation
directory cannot be uninstalled from this dialog. They must be manually removed from the
filesystem.


### Description Panel


Displays metadata about the extension selected in the Extensions List. The information
displayed is extracted from the `extensions.properties` file associated with the
extension.


The existence of this file is what tells Ghidra that the folder or zip file is a Ghidra
Extension. It is a simple property file that can contain the following attributes:


- **name**: Human-readable name of the extension. This is what will be displayed in
the dialog.
- **description**: Brief description of the extension.
- **author**: Creator of the extension.
- **createdOn**: Date of extension creation, in the format mm/dd/yyyy.
- **version**: The version of Ghidra for which this extension was built.


### Tools Panel


- ![Plus.png](../icons/Plus.png)  Allows the user to install a
new extension. An extension can be any folder or zip file that contains an
*extensions.properties* file. When one of these is selected, it will be copied to the
extension installation folder and extracted (if it is a zip).
- ![Refresh](../icons/reload3.png)  Reloads the Extensions
List


## Building Extensions


An extension is simply a Ghidra module that contains an `extension.properties` file.
Building an extension is very similar to building a ghidra module, which is done by using
`gradle`.


Ghidra includes a `Skeleton` module in the distribution that is meant to be used as
a template when creating extensions.   This module can be found at


`<GHIDRA_INSTALL_DIR>/Extensions/Ghidra`


Copy and rename this directory to get started writing your own module.  You can then use
`gradle` to build the extension by running this command from within your extension
directory:


`gradle -PGHIDRA_INSTALL_DIR=/path/to/ghidra/ghidra_<version>/ buildExtension`


**Related Topics:**


- [Configuring Tool Plugins](../Tool/Configure_Tool.md)
