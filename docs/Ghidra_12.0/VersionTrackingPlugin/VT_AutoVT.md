# Auto Version Tracking


The **Automatic Version Tracking**  uses various correlators in a predetermined order
to automatically create matches, accept the most likely matches, and apply markup. The following
correlators are run in this order if the associated [options](VT_AutoVT.md#auto-version-tracking-options) are set:


- [Exact Symbol Name Correlator](VT_Correlators.md#symbol-match)
- [Exact Data Correlator](VT_Correlators.md#data-match)
- [Exact Function Bytes Correlator](VT_Correlators.md#exact-function-bytes-match)
- [Exact Function Instructions Correlator](VT_Correlators.md#exact-function-instructions-match)
- [Exact Function Mnemonics Correlator](VT_Correlators.md#exact-function-mnemonics-match)
- [Duplicate Function Instructions Correlator](VT_Correlators.md#duplicate-function-instructions-match)
- [Data Reference Correlator](VT_Correlators.md#data-ref), [Function Reference Correlator](VT_Correlators.md#func-ref), **OR** [Combined Function and Data Reference Correlator](VT_Correlators.md#comb-func-data-ref)


If the Create Implied Matches option is set, Implied Matches will be created whenever
the above correlators accept matches.


If the Apply Implied Matches option is set, any created Implied Matches that have
the set minimum number of votes and does not exceed the set maximum number of conflicts
will be applied.


![](../shared/note.yellow.png) **NOTE: It is unlikely that all matches in the entire program will be made and there is no guarantee that no mistakes will be made. This
action was designed to try to save as much time as possible while also taking a conservative approach to the automation.**


## Auto Version Tracking Options


Auto Version Tracking will run each selected correlator and will use the option values found
in the Auto Version Tracking options rather than the options chosen when the correlators are
run individually. To access the options use Edit-&gt;Tool Options-&gt;Version Tracking-&gt;Auto
Version Tracking from the Version Tracking Match Window.


The following options are found when the **Edit-&gt;Tool Options-&gt;Version Tracking-&gt;Auto Version
Tracking** options folder is selected and will determine which correlators will be run during
Auto Version Tracking.


| Name | Description | Default Value |
| --- | --- | --- |
| **Create Implied Matches** | When true, Implied Matches will be created whenever the other correlators  			          accept matches. | `True` |
| **Run Duplicate Function Correlator** | When true, the Duplicate Function Instructions Correlator will be run  			          during Auto Version Tracking. | `True` |
| **Run Exact Data Correlator** | When true, the Exact Data Correlator will be run during Auto Version  			          Tracking. | `True` |
| **Run Exact Function Bytes Correlator** | When true, the Exact Function Bytes Correlator will be run during Auto  			          Version Tracking. | `True` |
| **Run Exact Function Instruction Correlators** | When true, the Exact Function Instruction Correlator and the Exact  			          Function Mnemonic Correlator will be run during Auto Version Tracking. | `True` |
| **Run Exact Symbol Correlator** | When true, the Exact Symbol Correlator will be run during Auto Version  			          Tracking. | `True` |
| **Run Reference Correlators** | When true, the Data Reference Correlator (if previous correlators applied  			          only data matches), Function Reference Correlator (if previous correlators  			          applied only function matches), or the Combined Function and Data Reference  			          Correlator (if previous correlators applied both data and function matches)  			          will be run during Auto Version Tracking. | `True` |


The following option is found when selecting
**Edit-&gt;Tool Options-&gt;Auto Version Tracking-&gt;Data Correlator Options**


| Name | Description | Default Value |
| --- | --- | --- |
| **Data Correlator Minimum Length** | This option sets the minimum data length used to find data matches when  			          running the Exact Data Correlator in Auto Version Tracking. | `5` |


The following option is found when selecting
**Edit-&gt;Tool Options-&gt;Auto Version Tracking-&gt;Exact Function Correlators Options**


| Name | Description | Default Value |
| --- | --- | --- |
| **Exact Function Correlators Minimum Function Length** | This option sets the minimum function length used to find function 	     			  matches when running the  Exact Function Instruction Bytes Correlator, the  	     			  Exact Function Instruction Correlator, and the Exact Function Mnemonics  	     			  Correlator  in Auto Version Tracking. | `10` |


The following option is found when selecting
**Edit-&gt;Tool Options-&gt;Auto Version Tracking-&gt;Duplicate Function Correlator Options**


| Name | Description | Default Value |
| --- | --- | --- |
| **Duplicate Function Correlators Minimum Function Length** | This option sets the minimum function length used to find function 	     			  matches when running the Duplicate Function Instruction Correlator in  	     			  Auto Version Tracking. | `10` |


The following option is found when selecting
**Edit-&gt;Tool Options-&gt;Auto Version Tracking-&gt;Symbol Correlators Options**


| Name | Description | Default Value |
| --- | --- | --- |
| **Symbol Correlator Minimum Symbol Length** | This option sets the minimum symbol name length used to find function 	   				 	and data matches when running the Exact Symbol Correlator in Auto Version  	   				 	Tracking. | `10` |


The following options are found when selecting
**Edit-&gt;Tool Options-&gt;Auto Version Tracking-&gt;Reference Correlators Options**


| Name | Description | Default Value |
| --- | --- | --- |
| **Reference Correlators Minimum Confidence** | This option sets minimum confidence score used to find function matches  			          using the Data Reference Correlator, the Function Reference Correlator and the  			          Combined Function and Data Reference Correlator. | `10.0` |
| **Reference Correlators Minimum Score** | This option sets minimum similarity score used to find function matches  			          using the Data Reference Correlator, the Function Reference Correlator and the  			          Combined Function and Data Reference Correlator. | `9.5` |


The following options are found when selecting
**Edit-&gt;Tool Options-&gt;Auto Version Tracking-&gt;Implied Match Correlator Options**


| Name | Description | Default Value |
| --- | --- | --- |
| **Apply Implied Matches** | This option if true, causes Auto Version Tracking to apply Implied Matches 			          if the minimum vote count is met and the maximum conflict count is not exceeded. | `True` |
| **Maximum Conflicts Allowed** | This option sets the maximum number of allowed conflicts for an applied  			          implied match in Auto Version Tracking. | `0` |
| **Minimum Votes Needed** | This option sets the minimum number of needed votes for an applied  			          implied match in Auto Version Tracking. | `2` |


Main content blockquote


*Provided by: *Version Tracking Plugin**


**Related Topics:**


- [Version Tracking
Introduction](Version_Tracking_Intro.md)
- [Version Tracking Tool](VT_Tool.md)
