[Home](../index.md) > [FunctionTagPlugin](index.md) > Function Tags

# Function Tag Window


The Function Tag window provides a list of function tags defined in the currently open
program. It will also show which tags are assigned to the currently-selected function. Tags may
be created by the user, or loaded from a predefined set (see section on [loading tags](#loading-tags) below).


To display the Function Tag window, select the **Window** → **Function Tags** option on the tool menu. Optionally, the
dialog may be activated by right-clicking on a function header in the listing and selecting the
**Edit Function Tags** option.


| ![](images/FullWindow.png) |
| --- |


## Window Components


- **All Tags**: Displays all tags that are available to assign to the
current function, as well as a count of the number of times each tag has been used
in the current program.
- **Assigned Tags**: Displays all tags that have been assigned to the current
function.
- **Functions**: Displays functions that contain any selected tags. If multiple
tags are selected, functions containing ANY of the tags will be displayed.
- **Tag Input Field**: Allows users to create new tags. Multiple tags may be created at one time.
![](images/InputField.png)


- **Action Buttons**


## Tag Operations


### Create


Tags can be created by using the *Tag Input Field* described above. Users may enter
multiple tag names delimited by a comma. All newly-created tags will be displayed in the
Available Tags List but are NOT yet assigned to any function.


> **Tip:** Each tag may have an associated comment that
is visible as a tooltip. This can be assigned after the tag has been created (see edit section below).


### Delete


Tags may deleted by selecting a set of tags and pressing the ![Delete](../icons/edit-delete.png) icon. Users will be prompted with the
following:


![](images/DeleteWarning.png)


If confirmed, the tag will be removed from the system and from all functions to which it had been assigned.


### Edit


Tag names and comments may be edited by double-clicking the item in the list. If the
tag is not editable the user will be presented with the following warning:


![](images/EditNotAllowedWarning.png).


If editing is allowed, the following dialog will be shown:


![](images/EditTag.png)


> **Tip:** An italicized tag name
indicates that the tag was loaded from an external source and has not yet been
added to the program, making it immutable. As soon as the tag is assigned to a function it becomes
editable. If you delete the tag using the icon it will be removed from
the program and once again be immutable.


### Add to Function


Tags may be added to a function by selecting a set of tags and pressing the  →  button. The tags will be
added to the Assigned Tags list, and shown as disabled in the Available Tags list.


### Remove from Function


Tags may be removed from a function by selecting a set of tags and pressing the  →  button. The tags will be
removed from the Assigned Tags List and added to the Available Tags List.


## Loading External Tags


Tags may be loaded on startup from an external source if desired. These tags will be shown with
an asterisk (*) after the name and cannot be edited or deleted; with one caveat: once a tag has
been assigned to a function it ceases to have any special protections and can be edited
like any other. If the tag is ever removed from all functions using the
![Delete](../icons/edit-delete.png) button, it will again be present in the
Available Tags list.


To make these available there must be a file named *functionTags.xml* available on
the classpath. Edit (or create) this file and add tags as needed. The format is
as-follows:


```

   <tags>
      <tag>
         <name>TAG1</name>
         <comment>tag comment</comment>
      </tag>
      <tag>
         <name>TAG2</name>
         <comment>tag comment</comment>
      </tag>
   </tags>

```


> **Tip:** Be aware that any external tags that have
removed/edited will reappear with Ghidra is restarted, as these are always loaded from this file.


*Provided By:  *FunctionTagPlugin**


**Related Topics:**


- [Functions](../FunctionPlugin/Functions.md)


---

[← Previous: Function Signature and Variables](../FunctionPlugin/Variables.md) | [Next: Set Register Values →](../RegisterPlugin/Registers.md)
