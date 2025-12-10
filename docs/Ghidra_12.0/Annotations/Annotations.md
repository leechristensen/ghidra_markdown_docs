# Annotations


Annotations are a method for embedding display markup in Ghidra fields, such as [comments](../CommentsPlugin/Comments.md). An annotation is written with a strict
syntax, which when rendered will have a display value as defined by the particular annotation
used. Furthermore, some annotations add functionality, such as making the display text a
hyperlink.


Annotation Example


The following text shows the syntax of a sample URL annotation:


```

	{@url "http://www.google.com" "Search Web"}

```


The bold text is required for all annotations. The italicized text is required but is
specific to the annotation being used (see the table below).  The optional rendered display text
"Search Web" will be displayed in listing.  If the optional display test is omitted, the URL
will be displayed.  Quotes around display text are optional.


## Examples


image


![](images/CommentDialogURLExample.png)

*URL Annotation Example*


The image above shows a URL annotation in its text form as entered into the EOL Comment
tab of the Comments dialog.


The image below shows how the annotation is rendered in Ghidra.


![](images/RenderedURLExample.png)

*Rendered URL Annotation Example*


When the URL text (e.g., "http://www.google.com") in the above image is clicked from within
Ghidra, a web browser is launched and attempts to load the corresponding web page.


If the URL text corresponds to a Ghidra URL and attempt will be made to open the referenced
Program file within the Code Browser.  Such a URL may refer to a Program file from a
local project or Ghidra Server.  The Ghidra URL forms supported include:


Remote Ghidra Server file

*ghidra://`<host>`[:`<port>`]/&lt;repository-name&gt;/&lt;program-path&gt;[#&lt;address-or-symbol-ref&gt;]*

Example: *ghidra://hostname/Repo/notepad.exe#entry*


Local Ghidra project file

*ghidra:/[&lt;project-path&gt;/]&lt;project-name&gt;?/&lt;program-path&gt;[#&lt;address-or-symbol-ref&gt;]*

Example: *ghidra:/share/MyProject?/notepad.exe#entry*


## Valid Annotations


List of Valid Annotations


The following is a table of supported annotations:


| Name   | Description   | Parameter List   | Accepted Keywords | Examples   |
| --- | --- | --- | --- | --- |
| Symbol   | Displays the text of the given symbol or the current name             of the primary symbol for a given address as a hyperlink.       Notes: If you provide a symbol name and not an address, then you will need to 		            fully-qualify the symbol name if it is not in the global namespace (e.g., 		            FunctionFoo::param1 to link to a specific function parameter).If you specify a symbol name instead of an address, then the text of the comment 		            will be changed to use the address of that symbol. | address or symbol name | @symbol@sym | {@symbol "0x1001004a"}{@symbol "fred"}{@sym "100100fe"} |
| Address   | Displays the given address value as a hyperlink.   | address[display text] | @address@addr | {@address "1001004a"}{@addr "0x0100100c"}{@address "01001004a" "my special address"} |
| URL   | Displays the given URL has a hyperlink. This annotation             optionally takes display text so that the hyperlink may be displayed with text other             than that of the URL.     References to a program file on a Ghidra Server ( *ghidra://&lt;host...* ) or              local project ( *ghidra:/&lt;project-...* ) will be opened within the Listing display,              while all other URL forms (e.g., *http://, https://, file://,* etc.) will be              launched via an external web browser (see [command configuration              for Processor Manuals](../ShowInstructionInfoPlugin/ShowInstructionInfo.md#processor-manual) ). | URL[display text] | @url@hyperlink@href@link | {@url "http://www.google.com"}{@url "http://www.google.com" "google"}{@url "http://www.google.com" "click here for google"}{@url "ghidra://myserver/Repo/notepad.exe"}{@url "ghidra://myserver/Repo/notepad.exe#entry"}{@url "ghidra://myserver/Repo/notepad.exe" "see notepad.exe"}{@url "ghidra:/share/MyProject?/notepad.exe#entry"}{@url "ghidra:/share/MyProject?/notepad.exe" "see notepad.exe"} |
| Program   | Displays a hyperlink to the given Ghidra program pathname              with the current project.  Referenced program              will open in a new Listing tab when clicked.   You may optionally provide an address or symbol to be displayed when the program is             opened by appending to the program name an '@' character, followed by an address or             symbol name. | program name (with optional address or symbol)[display text] | @program | {@program "WinHelloCPP.exe"}{@program "WinHelloCPP.exe@01001234"}{@program "WinHelloCPP.exe@some_label"}{@program "WinHelloCPP.exe@SomeFunction::some_label"}{@program "WinHelloCPP.exe" "Click here to open WinHelloCPP"}{@program "subfolder/WinHelloCPP.exe"}{@program "subfolder1/subfolder2/WinHelloCPP.exe"} |
| Execute   | Launches the specified executable with given optional             parameters.   | "executable path" **OR** "executable path""parameter list" (may be empty quotes)"display text" (may be empty quotes) | @execute | {@execute "C:\Program Files\Mozilla Firefox\firefox.exe"}{@execute "C:\Program Files\Mozilla Firefox\firefox.exe"                 "http://my.website.com" "Opens a web browser to Website"}{@execute "C:\Program Files\Mozilla Firefox\firefox.exe" "" "My display text"}{@execute "C:\Path\To\Some\executable.exe" "arg1 arg2" ""} Note: quotes are required for this annotation |
| *Discovered Annotations*   | Ghidra may discover new annotations that are provided by             Ghidra plugins. Consult the documentation of the respective plugins for more             information regarding the discovered annotations.   |  |  |  |


![Note](../icons/warning.help.png) All annotations support double
quotes (") around content inside of the annotation tag, excluding the **@*name***
part of the tag. Further, some annotations require quotes, as listed in the table above
(e.g., the **Execute** annotation requires quotes). It is considered good practice to
quote all annotation parameter values.


> **Tip:** When pressing the Add Annotation button, any selected text in the comment dialog will be added to the generated annotation.
This is useful if you wish to pre-selected content, such as address text, to be converted
into an annotation.


## Errors


If there is a problem parsing an annotation then an error message will be printed in place
of the annotations.


image


![](images/InvalidAnnotationsDialogExample.png)

*Invalid Annotation Text Entry*


image


![](images/RenderedInvalidAnnotation.png)

*Rendered Invalid Annotation Example*


**Related Topics:**


- [Comments Plugin](../CommentsPlugin/Comments.md)
