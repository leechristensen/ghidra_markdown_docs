[Home](../index.md) > [Tool](index.md) > Configure Tool

# Configure Tool


The *Configure Tool* dialog allows you to add/remove plugin packages or individual [Plugins](Ghidra_Tool_Administration.md#ghidra-tool-administration) from a tool. To
display the *Configure Tool* dialog, select **File**  → **Configure**.This dialog is also displayed when you [create a new
tool](Ghidra_Tool_Administration.md#create-tool).


![](images/ConfigTool.png)


<a name="stepstoconfiguretool"></a>


The *Configure Tool* dialog shows a list of plugin packages that can be added to
the tool. Clicking the unchecked checkbox will add all the plugins in the package that are
at the supported level (typically the RELEASED level) for that package.  Any plugins in the
package not at the supported level or higher will not be automatically added.  Clicking
the checked checkbox will remove all plugins from the tool that belong to that package.



Clicking on the **Configure** link will bring up a dialog for adding individual
plugins.


![](../shared/note.yellow.png)


#### Saving


<a name="savetool"></a> Save changes to your tool by clicking on the ![disk.png](../icons/disk.png) icon in the dialog's toolbar; [save your tool to a different
name](Ghidra_Tool_Administration.md#save-tool-to-tool-chest) by clicking on the ![disk_save_as.png](../icons/disk_save_as.png) icon.


#### Configuring All Plugins


<a name="configureallplugins"></a> To Configure all plugins regardless of package,
select the ![plugin.png](../icons/plugin.png) icon in the dialog's toolbar and the
*Configure Plugins* dialog will appear with all plugins in its plugin table.


![](../shared/note.yellow.png)The **Experimental** package can't be
added as a package. Experimental plugins must be added individually.


### Configure Plugins Dialog


Selecting the *Configure* link for a package will bring up the *Configure
Plugins Dialog*.


![](images/ConfigurePlugins.png)


The dialog has two parts: A table at the top of the dialog that shows of all the plugins
in the package and an information window at the bottom that shows details about an
individual plugin.


### Plugin Table


The plugin table shows the following information for each plugin:


- Checkbox to indicate whether the plugin is in the tool;
- A status icon:
  - none     - the plugin is good.  It has help and
been reasonably tested.
  - ![warning.png](../icons/warning.png)          -
the plugin is useable, but has not been fully tested and/or not
documented.
  - ![Strong Warning](../icons/software-update-urgent.png)          - the
<a name="developmentplugin"></a> plugin is under development and may not be usable
at all. Not included with production distribution.
- Plugin name: the name is displayed in red when some other plugin depends on this
plugin;
- Short description of the plugin;
- Category for where the plugin belongs functionally, e.g., it works in the context
of a Code Browser or Byte Viewer, etc.


The *<a name="searchfilter"></a> Search Filter* allows you to narrow the list of
plugins displayed in the table. Only those plugins whose name or description contains the
string that you enter as the filter will be displayed. As you type, the table is updated
to reflect the filter.


### Information Window


When you select a row in the table, the scrolled window below the table shows more
information about the plugin and any contact information that the author supplied, e.g.,
author's name, organization, etc.  The *Dependencies* section lists the class
names of the plugins that depend on the selected plugin due to some service that it
provides. The *Class Location* indicates from where the java classes are being
loaded.


**Related Topics:**


- [Create
Tool](Ghidra_Tool_Administration.md#create-tool)
- [Configure the Ghidra Project
Window](../FrontEndPlugin/Ghidra_Front_end.md)
- [Save Tool to Tool
Chest](Ghidra_Tool_Administration.md#save-tool-to-tool-chest)
- [Ghidra Tool
Administration](Ghidra_Tool_Administration.md)


---

[← Previous: Tools](Ghidra_Tool_Administration.md) | [Next: Default Tools →](Ghidra_Tool_Administration.md)
