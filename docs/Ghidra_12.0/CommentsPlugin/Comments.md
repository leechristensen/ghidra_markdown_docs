[Home](../index.md) > [CommentsPlugin](index.md) > Displaying Comment History

# Comments


Comments can be added to any instruction or data item. There are five categories of comments
that are supported:


| **End-of-line (EOL)**   | Displayed to the right of the instruction.   |
| --- | --- |
| **Pre**   | Displayed above the instruction.   |
| **Post**   | Displayed below the instruction.   |
| **Plate**   | Displayed as a block header above the instruction. Plate             comments are automatically surrounded by '*'s   |
| **Repeatable**   | Displayed to the right of the instruction if there is no             EOL comment. These comments are also displayed at the "from" address of a reference to             this code unit, but only if there is no EOL or repeatable comment defined at the from             address.   |


You can create, edit, or delete comments. You can also view a [history of comment changes](#displaying-comment-history) for each comment type. You may also use
[**annotations**](../Annotations/Annotations.md) to change the display
characteristics of data entered into the comment fields.


> **Note:** A comment can also be offcut. This means it is
defined on an address that is in the middle of an instruction or data item. In this case,
the offcut comment will be displayed in the appropriate field (EOL, PLATE, POST, PRE) on the
instruction or data that contains that address and will be colored red to indicate the comment
has been attached to an invalid address. Note that this comment can only be edited if the
containing instruction or data is first cleared so that the individual addresses are shown in
the listing.


## Adding or Editing Comments (Set Comment)


Comments can be added or edited using the *Set Comment(s)* dialog as follows:


1. From the right-mouse pop-up menu over the Code Browser window, select the
**Comments →  Set** menu
option.
2. Choose the appropriate tab for the type of comment that is to be added or edited.
3. Enter the comment text in the text window.
4. Press the **OK** button to save the changes and close the dialog.


| ![](images/Comment.png) |
| --- |


This dialog has the following keyboard shortcut behavior:


- When the *Enter accepts comment* checkbox is not selected, pressing **Enter**
simply adds newlines to the text; when the checkbox is selected, pressing **Enter**
will close the dialog and accept the current text without adding a newline.
- Pressing **Shift-Enter** will always insert a newline into the text
- Pressing **Control-Enter** will always close the dialog, accepting the current text


## **Deleting Comments**


Delete Comment will remove a specified comment from the listing. No confirmation is
displayed before the delete.


To Delete a Comment:


1. Right-click on the comment to be deleted.
2. Choose **Comments →  Delete
`<comment type>` Comment** from the popup-menu.


To undo a delete comment operation, use the [Undo Operation](../Tool/Undo_Redo.md).


## Navigating in the Code Browser


If a comment contains a string that can be interpreted as an address or a label, you can
navigate (in the [Code Browser](../CodeBrowserPlugin/CodeBrowser.md)) to
that address or label by double clicking on the address or label in the comment. If the
string matches more than one address or label, a [Query Results dialog](../Search/Query_Results_Dialog.md) displays the
matches.


## Displaying Comment History


Comment history is maintained for each change made to a comment. The history includes the
name of the user who made the change, the modification date, and the comment. Comment changes
are sorted in descending date order (most recent date first).


| ![](images/ShowCommentHistory.png) |
| --- |


To view the history of changes,


1. Right-click on the comment that you would like to view the history.
2. Choose **Comments →  Show History
for `<comment type>`...**.
- If you are not over a specific comment, right mouse click and choose
**Comments →  Show
History...**.
3. A dialog containing a tab for each of the comment types is displayed.
- If the comment does not contain history, then "No History Found" is shown in the
tabbed panel for that comment.
- Select a tab to view comment history for that comment type.


> **Note:** Only comments that are placed at the start
address of data or instructions are displayed.  Comments on addresses other than the start
(interior) address will remain hidden until the data or instructions are cleared.


*Provided by: *Edit Comments* Plugin*


Related Topics:


- [Bookmarks](../BookmarkPlugin/Bookmarks.md)
- [Browser Field
Formatter](../CodeBrowserPlugin/Browser_Field_Formatter.md)
- [Labels](../LabelMgrPlugin/Labels.md)
- [Annotations](../Annotations/Annotations.md)


---

[← Previous: Navigating in Codebrowser through Comments](Comments.md) | [Next: References →](../ReferencesPlugin/References.md)
