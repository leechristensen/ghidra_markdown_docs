[Home](../index.md) > [Intro](index.md) > Overview

# Introduction


Ghidra is a highly extensible application for performing software reverse engineering.
Ghidra is built upon a completely generic application framework. Application-specific
capabilities are provided by small software bundles called plugins, each providing one or more
features. This user's guide provides detailed information on how to use both Ghidra's generic
and reverse engineering-specific capabilities.


## Intended Audience


This guide is intended for anyone interested in learning how to use Ghidra to reverse
engineer a software system.


## Document Scope


The purpose of this document is to describe how to use Ghidra. It does NOT provide
information on the software architecture or the programming API.


## Disclaimer


Ghidra is configurable. At any given time, Ghidra capabilities can be added, removed, or
even replaced by changing the current set of plugins. Consequently, a feature might not be
available as described and the images shown in this document may not exactly match your
display.


# Getting Started


### File System Layout


In the directory you choose, a ghidra installation directory named
**ghidra_`<version>`** is created. The following directory structure will be created
under the Ghidra installation directory.


| docs | tutorial and on-line help |
| --- | --- |
| Extensions | installable extensions for Ghidra, Eclipse and IDA Pro |
| Ghidra | essential files for running Ghidra |
| GPL | GPL utility and support programs used by Ghidra |
| licenses | licenses for non-GPL portions of Ghidra |
| server | files required to launch and configure the Ghidra server |
| support | files useful for debugging and configuring Ghidra |


### Extensions


There are a number of Ghidra plugins that are not part of the base distribution. They
are either experimental, still under development, or contributed by others. These plugins
may not have been tested, and therefore may be unstable and are not included in any of the
default tools. However, these plugins often contain the more cutting edge features and may
be worth considering. They are easily accessible and can be added by [configuring](../Tool/Configure_Tool.md) a tool.


### IDA Pro Export


The Ghidra distribution includes a plugin for use with IDA Pro (a commercially available
disassembler). The XML plugin is used with IDA Pro to export IDA Pro databases as XML files
so that they can be imported into Ghidra. This allows IDA Pro users to migrate their data
to Ghidra.


To add the XML exporter plugin to your IDA installation:


- Locate the README file for your version of IDA from the version folders in the
`<ghidra installation directory>`/Extensions/IDAPro folder. The plugin is available
for IDA Pro versions 6 and 7. If you are unsure of your IDA version, start IDA and select
Help -&gt; About program ... from IDA's main menu to display the version.


To export data to Ghidra using the XML plugin, select File -&gt; Plugins -&gt; Dump
database as XML file... from IDA's main menu.


## Starting Ghidra


Launching Ghidra varies depending on the operating system.


### Ghidra on Windows:


Run the `ghidraRun.bat` file located in the Ghidra installation directory.


> **Tip:** One way to run this file is to use
the Windows file explorer to locate the ghidra.bat file and then simply double click on the
file .


### Ghidra on Linux and macOS:


Run the `ghidraRun` shell script file located in the Ghidra installation
directory.


Advanced startup parameters


### Advanced Startup


Ghidra provides some Java startup parameters which allow for the usage of advanced
features. To use a startup parameter you must open `support/launch.properties`
and add the parameter to that file.


For example,


```

               VMARGS=-Dfont.size.override=18


```


## Ghidra Overview


When Ghidra first starts, the *[Ghidra Project Window](../FrontEndPlugin/Ghidra_Front_end.md)* will
appear.


![](images/Empty_ghidra.png)

*Ghidra Front-End with no open project*


Ghidra is a project-oriented application and, consequently, all work must be performed in
the context of a project. Therefore, the first thing to do is to [create](../FrontEndPlugin/Creating_a_Project.md) a project or [open](../FrontEndPlugin/Opening_a_Ghidra_Project.md) an existing project. Once
a project is open, Ghidra will display the folders and data that make up the project along
with the user's current set of tools. Of course, newly created projects would not contain any
data. Data must be [imported](../ImporterPlugin/importer.md) into a
Ghidra project before any work can be performed. Importing data into a Ghidra project creates
*[programs](../Glossary/glossary.md#program)* that Ghidra [tools](../Tool/Ghidra_Tool_Administration.md) can manipulate.


![](images/Open_ghidra.png)

*Ghidra Front-End with an open project*


A Ghidra tool is a configuration of plugins that can be used to manipulate programs. When
Ghidra is first installed, a default tool - the code browser tool - is created for the user
and its icon is displayed in the Tool Chest area of the Ghidra Project Window.


To [run a tool](../Tool/Ghidra_Tool_Administration.md#run-tool),
click on its icon in the *Tool Chest.* When a tool is running, a new window will appear
for that tool and the tool's icon will be displayed in the *Running Tools* area of the
Ghidra Project Window.


Ghidra also supports the concept of *workspaces*. A [workspace](../FrontEndPlugin/Ghidra_Front_end.md#workspace) is simply a
collection of running tools that are visible on the desktop. Users can have multiple
workspaces, each with its own set of running tools. Running tools that are not in the current
workspace are still running and consuming system resources even though they are not
visible.


## Error Dialogs


Errors may occur in Ghidra. An error may be anticipated, or it may be unexpected in which
case it is a programming error. Each type of error is described below.


### General Errors


Whenever an action or operation does not complete as desired, but is an anticipated
error such as a user entering a file path that doesn't exist, Ghidra will display an Error
dialog explaining the cause of the problem as shown below in the sample error dialog:


![](images/Simple_err_dialog.png)


### Unexpected Programming Errors


Whenever an action or operation fails in a totally unexpected way, i.e., a programming
error, a dialog is displayed as shown below:


![](images/Err_Dialog.png)


The **Details** &gt;&gt;&gt; button expands the dialog to show the
details of the java stack trace. (The stack trace is also output to the console.)


---

[← Previous: Error Dialogs](Intro.md) | [Next: Docking Windows →](../DockingWindows/Docking_Windows.md)
