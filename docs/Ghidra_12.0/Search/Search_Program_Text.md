[Home](../index.md) > [Search](index.md) > Text

# Search Program Text


The Search for Program Text feature allows you to search for textual strings within [functions](../FunctionPlugin/Functions.md), [comments](../CommentsPlugin/Comments.md), [labels](../LabelMgrPlugin/Labels.md), [instructions](../Glossary/glossary.md#instruction), and [defined data](../DataPlugin/Data.md).   You can search incrementally or
get a list of all of the search results. You can search the entire program, or limit the search
to your current selection in the Code Browser.


To bring up the *Search Program Text* dialog, as shown below, select **Search** → **Program Text...** from the
tool menu.


![](images/SearchText.png)


### Search Type


There are two ways that you can search for text:  the *Program Database Search* and the
*Listing Display Search*.


The *Program Database Search* option searches the program database, not what you actually see in
the Code Browser.  Conversely, the *Listing Display Search* searches exactly what you
see in the Code Browser.  These searches yield different results because the listing includes derived and auto-generated
information that is not stored in the database and the database can contain information that is not currently displayed, such
as automatic comments.
The following table summarizes the pros and cons of using each
search type:


|  | **Program Database Search** | **Listing Display Search** |
| --- | --- | --- |
| **Advantages** | - Faster than theListing Display Search- Can search information that is not currently being displayed for various reasons  	            such as listing fields and display options. | - Search Results reflect what you see in the Code Browser Listing window.- Allows a search of all fields that are displayed in the Code Browser, which 	              includes auto generated and derived information that is not stored in the database. |
| **Disadvantages** | - Search Results may not match what the Listing displays, since this  				  search looks at information that is directly stored in the database and not the  				  derived and enhanced information that is shown in the Listing Display. Searches  				  are also restricted to specific fields and may not cover all the fields shown  				  in the Code Browser listing window.- Assumes a specificsearch orderof the fields; you 	              may have rearranged the fields in your Code Browser such that they appear in a 	              different order from the search order; this may cause cursor movement for incremental 	              searches to appear "random" within the content for a single address. | - Can be MUCH slower than a database search.  For example, 	            if you have a large program with one comment, the database search can find a match in that 	            comment instantly, while the listing display search will have to render every address in the 	            program one at a time until it finds a hit.- Does not find information that is currently not displayable by the Listing window.  For  	            example, comments at offcut locations are not displayed in the browser, so this search would 	            not find them. |


By default, the **Program Database** *Search Type* type is selected.


> **Note:** If you select the All Fields button, the Listing Display Search Type button automatically becomes
selected, as the Search All Fields does not apply to the Program Database . The Selected Fields option applies to either the Program Database or the Listing Display .


### Incremental Search


To search for text strings incrementally,


1. Select the **Search** → **Program Text** from the Code Browser
tool menu.
2. In the *Search for* field, enter the string for which you want to search, using
wildcards (* or ?) as needed. The * matches any character. The ? matches a single
character.
- This field does
not support *[regular
expressions](../Glossary/glossary.md#regular-expression)*.
- If you need to
search for one of the wildcard characters, then escape the character with a backslash.
For example, to search for any occurrence of an asterisk, you would enter `\*`
as the search string.
- Use the combo box next to the *Search for* field to view the list of search
strings that you previously entered.
- If you have selected text within
a single field, then if you invoke the dialog, it will automatically load that text into the
*Search for* text box for your convenience.
3. Select the options for where in the Program to search.
- Functions - search function headers, comments, signature, variable types, variable
names, and comments on variables
- Comments - search Plate, Pre-, Post-, End of Line Comments, and Repeatable; by default this check box
is selected
- Labels - search Labels
- Instruction Mnemonics - search the Mnemonics of instructions
- Instruction Operands - search the Operands of instructions
- Defined Data Mnemoncis - search Mnemonics of defined data
- Defined Data Values - search Values of defined data
- The **Program Database**
*Search Type* does not include components of  [Structures](../DataPlugin/Data.md#structure) or [Unions](../DataPlugin/Data.md#union). Use the
**Listing Display** *Search Type* for this case. If you do want to
search structures or unions, they
must be open in the Code Browser.
- If you have made a selection and it
has been loaded into the *Search for* text box then the dialog will
automatically select the field that the text was found in as your choice of
*Field* to search. You have the option to add more or remove this selection
if you wish.
4. Select whether or not to search "Other" memory blocks (blocks that not actually
loaded in a running program); *Loaded Blocks* is selected by default which means
"Don't search the "Other" blocks.
5. You can select or deselect the *Case Sensitive* check box depending on whether you
want your search to consider case.
6. If you make a selection in the Code Browser, the *Search Selection* check box will
be selected by default. If you do not want the search to be restricted to the selection,
then deselect the check box.
7. Click on the **Next** or **Previous** button to search
forwards or backwards in the program, (or from the *Search for* field,
press the **`<Enter>`** key to search forward).
- The start of the search operation begins at your current location in the Code
Browser.
8. If a match is found, the current location in the Code Browser is moved to the location
of the match. If no match is found, then a "Not found" message is displayed in the
dialog.
9. If you mouse click in the Code Browser to move focus
there, you can choose **Search** → **Repeat Text Search** to go to the next match found.


> **Note:** Search operations do not
"wrap" once the you have reached the maximum address in memory or within a selection. Select
the Backward direction check box to search backwards from your current location.


> **Tip:** For very large Programs
that may take a while to search, you can cancel your search at any time. For these
situations, an indicator for "search in progress" is displayed with a Cancel button. Click on the Cancel button to stop
the search


> **Note:** Dismissing the search
dialog automatically cancels the search operation. For search all ,
partial results are ignored if the search dialog was dismissed while the search was still in
progress, therefore, the "View Results" question dialog will not be displayed.


### Search All


- To find all matches in the Program (or a selection in the program),


1. Follow the Steps 1 through 6 for [searching
incrementally](#incrementalsearch). (Skip Step 4 as *Direction* is irrelevant in this case.)
2. Click on the **Search All** button.
3. The *[Query
Results](Query_Results_Dialog.md)* display shows all the matches.


![](images/QueryResultsSearch.png)


> **Tip:** When performing a "Search All" on large Programs,
the results table will appear before the search is completed.  At the bottom of this window,
there will be a cancel button that you can use to stop  the search.


There may be multiple entries for the same address, depending on what you search for. For
example, a string may appear multiple times in the same pre-comment, so you will see as many
entries in the Query Results display. When you click on a row in the *[Query Results](Query_Results_Dialog.md)* display, your cursor in the Code Browser is
moved to that location where the match was found. So, if the match was found in an operand,
then the location is moved to the matching string within the operand.


### Search Limit Option


The tool has an option to limit the number of search results. The search will stop after
this number has been exceeded. The below dialog warns you of the partial results. To see more
search results, select **Edit** → **Tool
Options...** from the menu bar, then select the *Search* node in the tree. Edit the
*Search Limit* field to increase your search limit.


![](images/SearchLimitExceeded.png)


### Highlight Search Option


You can specify that the string found in the search be highlighted by selecting the
*Highlight Search Results* checkbox on the Search Options panel. To view the Search
Options, select **Edit** → **Tool Options...** from the tool menu, then select the *Search* node in the Options
tree in the Options dialog. You can also change the highlight color. Click on the color bar
next to *Highlight Color* to bring up a color chooser. Choose the new color, click on
the **OK** button.  The option for *Highlight Color for Current Match* indicates
the color used to highlight the match when it occurs at the current location in the Code
Browser.  Apply your changes by clicking on the **OK** or **Apply** button on the
Options dialog.


The highlight options also apply to [searching memory](Search_Memory.md).


> **Tip:** Other notes of interest
on highlighting:


- Highlights are displayed for the last search that you did. For example, if you bring up
the Search Memory dialog and search for bytes, that string now becomes the new highlight
string. Similarly, if you invoke [cursor text
highlighting](../CodeBrowserPlugin/CodeBrowser.md#cursor-text-highlight), that becomes the new highlight string.
- Highlights are displayed only for those items that you selected to search.  For
example, you did not select *Labels* to search but a label matched the string you
searched for.  Thus, the field for that label will not be highlighted.
- Highlights are dropped when you close the search dialog, or close the query results
window for your most recent search.


### Default Search Order for *Program Database Search*


For the *Program Database Search* option, as you incrementally step, the order in which the
cursor is positioned at the match in the Listing fields is as follows:


- Functions
- Plate Comments
- Pre-Comments
- Labels
- Instruction Mnemonic
- Instruction Operands
- Defined Data Mnemonics
- Defined Data Values
- End of Line Comments
- Repeatable Comments
- Post Comments


Within a Function, the order is as follows:


- Function Comments
- Function Signature
- Stack Variable Type
- Stack Variable Name
- Stack Variable Offset
- Stack Variable Comment


The *[Query Results](Query_Results_Dialog.md)* display will show the
search results in this default search order.


> **Note:** If your Listing fields are
organized in a different order from the search order (e.g., Plate Comment is after the End of
Line Comment), then as you search incrementally, your cursor potentially would move back and
forth at the same address where there are multiple matches all at the same address. In this
case, the cursor movement may look "random." This is the case only for Program Database Search ;
the Listing Display Search searches in the order of the displayed fields in the Listing.


*Provided By:  *TextSearchPlugin**


**Related Topics:**


- [Query Results](Query_Results_Dialog.md)
- [Data](../DataPlugin/Data.md)
- [Listing Fields](../CodeBrowserPlugin/Browser_Field_Formatter.md)
- [Search Memory](Search_Memory.md)


---

[← Previous: Memory](Search_Memory.md) | [Next: Search and Replace →](SearchAndReplace.md)
