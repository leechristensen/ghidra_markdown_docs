[Home](../../index.md) > [VersionTrackingPlugin](../index.md) > Matches Table

# Version Tracking Matches Table


The Version Tracking Matches Table is the primary window for managing a version tracking
session.  It displays a list of all matches contained in the current session.  All other
version tracking windows are driven by selecting a match within this table.  This window
is also the primary means for accepting matches and bulk applying markup items. In addition,
this table provides an extensive filtering system.


| ![](../images/MatchesTable.png) |
| --- |


## Version Tracking Match


A match represents an opinion that a function or data in one program is the equivalent
function or data in another program.  The pairing of a function or data from one program to
another is called an association. There can be multiple matches (opinions) for the same
association by one or more correlation algorithms.  When a match is considered correct, it
should be marked as accepted.  When a match is marked as accepted, it is really the
association that is accepted and therefore all matches that have the same association are
considered accepted. Also, when a match is accepted, all competing matches (matches that have
the same source or destination address, but not both) become blocked.  For example, if one
match has the opinion that A in one program is associated with X in another program and
another match has the opinion that A is associated with Y, then accepting the first match,
will block the second match since A can't be associated with both X and Y.


## Match Status


Each match has a primary status that is one of **Available, Accepted, Rejected, or
Blocked**. In addition, matches that are **Accepted** have additional status for its
markup items. The status column uses overlayed icons to provide information about both
types of status. The table below lists the various combined status of a match.


| Status | Icon | Description |
| --- | --- | --- |
| AVAILABLE |  | The match is available to be accepted and applied. |
| REJECTED | ![dialog-cancel.png](../../icons/dialog-cancel.png) | The match has been rejected by the user. |
| BLOCKED | ![kgpg.png](../../icons/kgpg.png) | The match can't be accepted because a conflicting match has been accepted.     Note: To see which associations are causing a blocked association, sort the table 	          by source or destination address to see all conflicting associations. |
| ACCEPTED | ![flag.png](../../icons/flag.png) | The match has been accepted. |
| ACCEPTED - Not Done |  | The match has been accepted. There is at least 1 markup item that has not been examined. |
| ACCEPTED - Fully considered | ![](../images/accepted_fully_considered.png) | The match is accepted and all markup items have been applied or ignored. |
| ACCEPTED - Fully Applied | ![](../images/accepted_fully_applied.png) | The match is accepted and all markup items have been applied. |


## Match Table Columns


| Column Name | Description |
| --- | --- |
| Session ID | A one-up number for the correlation algorithm run this match belongs to. |
| Status | The match status. See the section above on [Match Status](#match-status) |
| Type | Type of match.  Either function or data |
| Source Label | The label at the source address of this match. |
| Dest Label | The label at the destination address of this match. |
| Multiple Source Labels? | Icon indicating there is more than one label at the match's source  	          address and a number indicating how many labels. The tooltip can be viewed to see  	          the label names. |
| Multiple Dest Labels? | Icon indicating there is more than one label at the match's destination  	          address and a number indicating how many labels. The tooltip can be viewed to see  	          the label names. |
| Score | The primary similarity score for this match. The value will be between 0.0 and 1.0. This score 	          indicates how similar two match items are, not necessarily that they are THE correct match. Scores should NOT be compared 	          between different correlator algorithms. |
| Confidence Score | A score where higher numbers indicate more confidence that the two items are a match.  These numbers have no intrinsic  	          meaning other than higher numbers are better for the same correlator algorithm.  Confidence scores should NOT be compared 	          between differrent correlator algorithms. Typically, this number 	          is a combination of the similarity score and some length indicator or the number of duplicate matches. |
| Source Length | The length of the source function or data item. |
| Dest Length | The length of the destination function or data item. |
| Votes | The number of references from previously accepted matches that would suggest 	          that this is a correct match. |
| Source Address | The address of the function or data object in the source program. |
| Destination Address | The address of the function or data object in the destination program. |
| Algorithm | The algorithm that was used to generate this match. |
| Length Delta | The difference in lengths between the source and destination objects. |
| Source Label Type | The source of the label in the source program.  (Imported, Analysis, User Defined, etc.) |
| Destination Label Type | The source of the label in the destination program.  (Imported, Analysis, User Defined, etc.) |
| Markup Status | Displays an overview of the markup items status.  There is a colored 	          orb for each status type and that orb is either colored if at least one markup item 	          has that status or else it is greyed out. An orange orb indicates that one or more 	          markup items have 	          been applied or marked.  A green orb indicates at least one markup item has 	          been applied.  A purple orb indicates markup items that are rejected. A blue orb 	          indicates there are markup items that have been ignored (either "Don't Know" or "Don't  	          Care". And finally, a red orb indicates that at least one markup item could not be 	          applied due to some error. |
| # Conflicting | The number of unique associations with either the same source or same destination address.     This is the number of associations that will become [BLOCKED](#blocked) if you accept the match 	          in this row of the table. |


## Match Table Actions


The **Accept Match**
![flag.png](../../icons/flag.png)
action marks a match (and all matches that have the same association) as being
accepted.  All competing matches will become blocked.
[There are options](VT_Apply_Options.md#accept-match-options) to auto-apply
function names and create implied matches when accepting a match.


The **Apply Blocked Match**
[Blocked]


The **Apply Markup**
![checkmark_green.gif](../../icons/checkmark_green.gif)
action will attempt to apply all the markup items for the match
[according to the apply settings](VT_Apply_Options.md#apply-markup-options).
If the match is not already accepted, it will first be marked as accepted.


The **Reject Match**
![dialog-cancel.png](../../icons/dialog-cancel.png)
action will mark the match as rejected.


The **Choose Match Tag**
![tag_blue.png](../../icons/tag_blue.png)
action allows the user to set a user-defined tag that has been created via the [Edit Tag](#edit-tag) action.


The **Remove Match Tag**
![tag_blue_delete.png](../../icons/tag_blue_delete.png)
action removes any tag associated with the selected match(es)


The **Edit Tag**
![tag_blue_edit.png](../../icons/tag_blue_edit.png)
action allows the user to manage (create and delete) custom tags that can be applied to
matches.


The **Clear Match** ![undo-apply.png](../../icons/undo-apply.png)
action will reset the match to unaccepted and undo any applied markup.


The **Remove Match** ![edit-delete.png](../../icons/edit-delete.png)
action will remove the selected match(es).


> **Warning:** As of Ghidra 11.2, Version Tracking supports deleting matches.  Any match that has
not been accepted can be deleted without confirmation.   However, if you attempt to
delete an accepted match that is the last match for an association , then
you will be prompted to confirm your decision.


Generally, we suggest users should not delete accepted matches for the following reasons:


- Accepted matches are used by some of the other correlators to find more matches. If
completely deleted, those other correlators will not have as much information to work
from.
- The number of implied match votes and conflicts will be altered when accepted
matches are completely removed.
- If deleting an accepted match causes the number of votes to reach
zero for a particular implied match, the implied match will be deleted as well.
- Selecting an accepted match in the match table allows users to see what markup was
applied when the match was accepted. Deleting accepted matches while keeping applied
markup will remove this supporting evidence regarding how the markup was generated.


> **Tip:** An alternative to deleting matches is to
simply filter them out of the table once they have been applied. You can also tag
any matches you wish to ignore and then use the advanced filters to hide any matches with those tags.


It is important to understand what happens in Version Tracking when deleting a match.
You will have to make a decision before deleting whether you want to keep any changes
made to the destination program when you accepted a given match or whether you wish to
remove that markup.  When deleting an accepted match:


To keep all applied markup, simply delete the match and, when
prompted, choose **Delete Accepted Matches**.  This choice will delete the match and
its markup items, but **any applied markup item content will remain in the destination
program.**  Alternatively, when prompted, you can choose **Finish** which will
close the prompt dialog and will not delete the remaining accepted matches or markup.


To remove all applied markup, then you must first
[clear](#clear-match) the match before executing the remove action.  The clear
action will remove applied markup.  After clearing the match, then you can remove
the match and no markup will remain in the destination program.


The **Make Selections** ![Make Selection](../../icons/stack.png)
action will create selections in the source and destination tools for all matches selected in the table.


The **Table Selection Mode**
![table_gear.png](../../icons/table_gear.png) allows you to change the behavior
of the match table with regard to how it tracks table selections as you apply
matches.


As you make changes to a match, the table will update.   Sometimes as the table
updates the changed match will disappear from the table (for example, if your filter
settings are setup to hide applied matches and you have just applied a match).  The
default behavior (![table_gear.png](../../icons/table_gear.png)) is to keep
the table selection on the same row, regardless of whether
the match changes its position in the table or is removed from the table altogether.


Table Selection States:


| Action Icon | Action Name | Description |
| --- | --- | --- |
| ![table_gear.png](../../icons/table_gear.png) | Track Selected Index | Causes the match table to maintain the selection for  			        		the selected **row** .  So, for example, if you change a match, and that  			        		match is moved as a result of the table re-sorting, then the selection  			        		will remain on the row where the applied match used to be. |
| ![table_go.png](../../icons/table_go.png) | Track Selected Match | Causes the match table to maintain the selection for  			        		the selected **match** .  So, for example, if you change a match,  			        		and that match is moved as a result of the table re-sorting, then  			        		the selection will change to keep the applied match selected. |
| ![table_delete.png](../../icons/table_delete.png) | No Selection Tracking | In this state the table will not restore selections.   			        			If changes are made to matches, the selection will be lost. |


The **Settings** ![settings16.gif](../../icons/settings16.gif)
action will bring up the version tracking accept and apply options.


The **Compare Functions**
action allows users to visually compare selected matched functions. To initiate this action,
select one or more matches from the Version Tracking Matches Table, then choose
**Compare Functions** from the pop up menu. This will open a new
[Function Comparison](../../FunctionComparison/FunctionComparison.md)
table containing a list of source functions and a list of destination functions.
The user can choose one from each list at a time to visually compare to each other.
Note: You cannot compare Data matches or External Functions using this action, so
if you select either of these as matches they will not be populated in the table.


## Match Filters


### Table Filters


The match table has an extensive assortment of filters. There
are several commonly used filter controls at the bottom of the table:


1. **Text Filter** - allows you to filter based on any text in the table
2. **Score Filter** - allows you to filter on a range of scores.  All scores
are between 0 and 1
3. **Confidence Filter** - allows you to filter a range of confidence values.
All confidence values will be greater than -9.999 and smaller than 9.999.
4. **Length Filter** - is used to filter out
functions that are smaller than some number


### Advanced Filters


Finally, the ![Unfiltered](../../icons/lightbulb_off.png) will show the ancillary filters
available. The table below lists and describes the available filters. When an ancillary
filter is applied, the icon will change to ![Filtered](../../icons/lightbulb.png) .
Further, the icon may occasionally flash as a reminder that there is a filter applied.


| Filter Name | Description |
| --- | --- |
| Match Type | This filter allows the user to show only function or data matches. |
| Association Status | This filter allows the user to show only matches whose assocation 		          	has one of the included status types.  A useful setting 		          	for this filter is to turn off all but the **Available** status.  This will cause the 		          	table to act like a "To Do" list. |
| Symbol Type | This filter allows the user to show only matches whose source or  		          destination labels are of one of the included symbol types. |
| Algorithms | This filter allows the user to show only matches that were generated 		          by one of the included types of correlating algorithms |
| Address Range | This filter allows the user to show only matches whose source or 		          destination address is within the specified range. |
| Tags | This filter allows the user to show only matches whose tag is an 		          included tag. |


### Table Column Filters


The matches table also supports
[Table Column Filters](../../Trees/GhidraTreeFilter.md#column-filters) for creating complex filters for individual table columns.


end of top-level blockquote


*Provided by: *Version Tracking Plugin**


**Related Topics:**


- [Version
Tracking Markup Items Table](VT_Markup_Table.md)
- [Version Tracking Tool](../VT_Tool.md)
- [Version
Tracking Introduction](../Version_Tracking_Intro.md)


---

[← Previous: Tool](../VT_Tool.md) | [Next: Markup Items Table →](VT_Markup_Table.md)
