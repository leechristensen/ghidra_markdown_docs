[Home](../index.md) > [VersionTrackingPlugin](index.md) > Preconditions

# Version Tracking Preconditions


One of the first items you run across in the Version Tracking Wizard is the
Precondition Panel.
***Put picture here****
It is an important initial step in the Version Tracking process. In the past, users
trying to match functions and pull relevant "mark-up" such as labels and comments into a
new version of a binary, would encounter problems if one or both of the binaries were not
sufficiently analyzed or had major analysis problems. Users were given no indication that
these issues were a direct result of having a poorly analyzed binary. The success or failure
of the various preconditions are indicatiors of how well your binaries have been analyzed
and how well their analyses "match" each other. If the preconditions indicates problems
*** show and describe red x, warning, green check****, it is important to fix them before
moving on or there will probably be problems with the Version Tracking process, such as
identifying incorrect matches or failing to find valid function matches. In general,
Version Tracking will work best if the same methods of cleaning up a binary are used and
if similar numbers of functions are created.


## Current Preconditions


| Precondition Name | Precondition Description | Potential Problems | How to Fix |
| --- | --- | --- | --- |
| **Memory Blocks** | This validator checks to see if both program memory maps have been split into the same memory blocks with the same permissions. | Potential problems include incorrect analysis and decompilation due to incorrect execution or data permissions being set. | Use the Window-&gt;Memory Map to adjust the memory blocks and permissions so that they are correct. |
| **Number of Functions** | This validator checks to see if both programs have a similar number of defined functions | Potential problems include missing function matches. | Change analysis options and rerun it, run analysis scripts, run aggressive analyzer, and/or manually disassemble and create functions. |
| **Number of "No-Return" Functions** | This validator checks to see if both programs have a similar number of "No-Return" functions | Potential problems include bad analysis due to disassembly falling through past the end of a function. | Run the FixupNoReturnsScript. |
| **Offcut References** | This validator checks to see if either program has offcut references. | Potential problems include bad analysis due to disassembly or data creation in incorrect locations. | Using the Symbol Table find offcut references. If they are incorrect, fix them and the problems that caused them to be created such 			          as incorrect operand reference assumptions or incorrect memory map flags, etc... |
| **Percent Analyzed** | This validator checks to see if both programs have a similar percentage of analyzed code in the code segments of each binary. | Potential problems include missing potential matches due to incomplete analysis. | Change analysis options and rerun it, run analysis scripts, run aggressive analyzer, and/or manually disassemble and create functions. |
| **Red Flags** | This validator checks to see if either program has red flags indicating errors in analysis. | Potential problems include incorrect instruction definitions at the language level and incorrect analysis of code or data. | Use the Bookmark Manager or Margin Markers to find red flags. Fix them and the problems that caused them to be created such 			          as bad flow (most likely) or bad instruction definitions. |


*Provided by: *Version Tracking Plugin**


**Related Topics:**


- [Version Tracking Matches Table](providers/VT_Matches_Table.md)
- [Version
Tracking Markup Table](providers/VT_Markup_Table.md)
- [Version
Tracking Introduction](Version_Tracking_Intro.md)
- [Code Browser](../CodeBrowserPlugin/CodeBrowser.md)


---

[← Previous: Workflow](VT_Workflow.md) | [Next: Example Workflow →](VT_Workflow.md)
