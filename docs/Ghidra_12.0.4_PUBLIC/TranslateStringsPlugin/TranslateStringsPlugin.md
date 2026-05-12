[Home](../index.md) > [TranslateStringsPlugin](index.md) > Translate Strings

# Translate Strings


The Translate Strings Plugin provides a framework to allow strings found in a program to be
decorated with an alternate value that is more meaningful to the Ghidra user.


This plugin doesn't perform any natural language translation by itself.  The
user must install **string translation service**s that do the actual translation.
Extensions to Ghidra are installed via the **File
→  [Install Extensions](../FrontEndPlugin/Extensions.md)**
menu.


When a string has been translated, the translated value will be shown in place of
the original value, bracketed with **»chevrons«**


## Translate Menu


The **Data  →
Translate** menu will appear in the popup menu of the **Listing**
window when a string or string-like datatype is selected, and in the **Defined Strings**
table (found under **Window
→  Defined Strings**).


### Manual string translation


Allows the user to specify a translated string value manually, by typing a value
in a pop-up dialog.


Select an existing string instance in the **Listing** window and right click
and select **Data  →
Translate  →
Manual** to enter a manual translation.


In the **Defined Strings** table select a row or a range of rows and right
click and select **Translate
→  Manual**.


### Clear translated values


Removes the stored translated value for the selected string data instances.


The selected string instances will default back to their true value.


Select an existing string instance in the **Listing** window and right click
and select **Data
→  Translate
→  Clear translated values**
to clear the translated value.


In the **Defined Strings** table select a row or a range of rows and right
click and select **Translate
→  Clear translated values**.


### Toggle show translated values


Toggles the display of the translated string with the original value.


Select an existing string instance in the **Listing** window and right click
and select **Data
→  Translate
→  Toggle show translated values**
to toggle the display of the translated value of each of the strings.


In the **Defined Strings** table select a row or a range of rows and right
click and select **Translate
→  Toggle show translated values**.


## String translation services


String translation services, which are separate from this Translate Strings Plugin,
can be installed that will allow the user to translate strings.


Once installed, the translation service plugins, like all plugins, can be
found in the **File  →
Configure** window and must be enabled before they will
appear in the **Data  →
Translate** menu.


Each string translation services will operate in a different way, please consult
the documentation from the service for specifics.


The **Manual** string translation service is always available.


## Creating a String translation service


Please see the SampleStringTranslationPlugin.java source file for an example of
how to create your own translation service.


Alternatively, you could customize the TranslateStringsScript.java file and
operate directly on the string instances without using this plugin.


*Provided by: *Translate Strings Plugin**


**Related Topics:**


- [Code Browser](../CodeBrowserPlugin/CodeBrowser.md)
- [View Defined Strings](../ViewStringsPlugin/ViewStringsPlugin.md)


---

[← Previous: Data Types](../DataPlugin/Data.md) | [Next: LibreTranslate →](../LibreTranslatePlugin/LibreTranslatePlugin.md)
