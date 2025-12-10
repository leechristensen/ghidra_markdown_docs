[Home](../index.md) > [GhidraScriptMgrPlugin](index.md) > Ghidra Script Development

# Ghidra Script Development


Ghidra provides built-in support for creating scripts using the Java language and
add-on packages to support other scripting languages.


## Creating Scripts in Java


In order to write a script in Java:


1. Your script class must extend `ghidra.app.script.GhidraScript`.
2. You must implement the `run()` method. This is where you insert your
script-specific code.
3. Of course if you choose Java, the Ghidra script must be written in Java.
An implementation for Python (based on Jython) is also provided.


![](images/New_Script_Editor.png)


## Tips


Classes for performing file I/O are located in the java.io package.


To develop using the Eclipse IDE, instead of a simple text editor, install the
developer add-on package. Next, install the GhidraDev plugin for Eclipse. If you don't already
have Eclipse, you will need to install this separately.
The GhidraDev extension is distributed in `<GHIDRA_INSTALLATION>/Extensions/Eclipse/GhidraDev`.
Please see the README.
This is highly recommended if you plan to do more than simple edits to scripts.


## Meta-data


The scripting framework supports special meta-data comments. These comments are
treated specially by the script manager.


1. Each line of meta-data should start with the scripting language comment character. For
example, in Java line comments start with "//".
2. The first portion is the description.
3. The first line that starts with "@" terminates the description.


The available tags are listed below:


**`@author`**


This tag indicates the author of this script. It may include contact information.


**`@category`**


This tag indicates the category path for this script. Category levels are delimited
using the "." character.


For example, `"@category categoryA.categoryB"`.


**`@importpackage`**


This tag is used to declare [inter-bundle dependencies](../BundleManager/BundleManager.md#inter-bundle-run-time-dependency) as a comma separated list of Java packages. The complete syntax is that
of the [`Import-Package` attribute](https://osgi.org/specification/osgi.core/7.0.0/framework.module.html#framework.module.importpackage) in an OSGi bundle manifest.


For example:


`
@importpackage org.my.script.library
@importpackage org.my.script.library,org.your.script.library
@importpackage org.apache.commons.collections.properties;version=4.4
@importpackage org.ghidra.analysis;version="[1.1,2)"
`


**`@keybinding`**


This tag indicates the default keybinding that will activate this script. If the
Script Manager is unable to interpret the keybinding, it will be ignored. The format for
the key binding is ["ctrl"] ["alt"] ["shift"] [A-Z,0-9,F1-F12]. The format string is not
case-sensitive.


For example:


`@keybinding ctrl shift H
@keybinding ctrl alt shift F1
@keybinding L
@keybinding ctrl shift COMMA
`


**`@menupath`**


This tag indicates the top-level menu path. Path levels are delimited using the "."
character. A mnemonic can be defined by adding an ampersand ("&") in front of the mnemonic
key. Ampersands can be escaped by adding another ampersand ("&&").


For example:


`@menupath File.Run.My Script
@menupath File.Run.My &Script
@menupath File.Run.Me && My &Script
`


`@toolbar`


This tag indicates a top-level toolbar button should be created to launch this script
and the image to use for the button. The Script Manager will attempt to locate the image
in the [Script Directories](GhidraScriptMgrPlugin.md#script-directories-bundle-manager) and
then in the Ghidra installation. If the image does not exists, a toolbar button will be
created using the default Ghidra ![core.png](../icons/core.png) image.


For example, `"@toolbar myScriptImage.gif"`.


`@runtime`


This tag indicates which Ghidra script runtime environment is required to execute the
script. It allows for greater control when more than one Ghidra script runtime environment
uses the same script file extension. If left unspecified, the first Ghidra script runtime
environment that matches the script's extension will be used.


For example, specify `"@runtime Jython"` if the script is targetted for a Jython 2
runtime environment rather than a Python 3 runtime environment.


## Supporting Other Languages


The scripting framework can be extended to support scripts written in other languages.


In order to write scripts in other languages, you must extend `ghidra.app.script.GhidraScriptProvider.`


The methods that must be overridden are:


### File createNewScript()


Creates a file containing a new template in the script language


### String getCommentCharacter()


Returns the comment character used in the script language. For example, "//" or "#".


### String getDescription()


Returns of description of the script language. For example, "JAVA" or "Python".


### String getExtension()


Returns the file extension for script language. For example ".java" or ".py".


### GhidraScript getScriptInstance(File sourceFile, PrintWriter writer)


Returns a new instance of the GhidraScript


**Related Topics:**


- [Scripting](GhidraScriptMgrPlugin.md)


---

[← Previous: Console](../ConsolePlugin/console.md) | [Next: Ghidra Bundles →](../BundleManager/BundleManager.md)
