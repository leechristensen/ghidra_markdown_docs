[Home](../index.md) > [BSimCorrelator](index.md) > BSim Program Correlator

# BSim Program Correlator


The BSim [Program
Correlator](../VersionTrackingPlugin/VT_Correlators.md) uses the decompiler to generate confidence scores between potentially matching
functions in the source and destination programs. Function call-graphs are used to further
boost the scores and distinguish between conflicting matches.
.


The decompiler generates a formal feature vector for a function, where individual features
are extracted from the control-flow and data-flow characteristics of its normalized p-code
representation.


Functions are compared by comparing their corresponding feature vectors, from which
similarity and confidence scores are extracted.


A confidence score, for this correlator, is an open-ended floating-point value
(ranging from -infinity to +infinity) describing the amount of correspondence between the
control-flow and data-flow of two functions. A good working range for setting thresholds
(below) and for describing function pairs with some matching features is 0.0 to 100.0.
A score of 0.0 corresponds to functions with roughly equal amounts of similar and dissimilar features.
A score of 10.0 is typical for small identical functions, and 100.0 is achieved by pairs
of larger sized identical functions.


The correlator initially collects high confidence (high scoring) matches as a "seed" set.
Then, using call-graph information, the seed matches are extended to additional matches
throughout the programs.


There are four options for the BSim Program Correlator:


**Confidence Threshold for a Match**


This option sets the threshold for accepting
a new match by following the call-graph from a previously accepted pair of matching functions.
Because potential pairs are drawn from the local call-graph neighborhood of an
accepted pair, this threshold is typically set lower than the seed threshold.


**Confidence Threshold for a Seed**


This establishes the threshold for choosing
potential matches as part of the initial "seed" set. Be careful setting this threshold
lower than the default, as any false match in the initial seed set is more likely to propagate.


**Memory Model**


The memory model option selects how much memory to use for finding
matches. If you run out of memory correlating large programs, lower this choice to "Medium"
or "Small"...note however that correlation may be slightly less accurate.


**Use Accepted Matches as Seeds**


This option indicates whether to include
previously accepted matches, typically from other correlators, into the initial "seed" set.
The BSim Program Correlator will still try to find additional seed matches to merge
with the already accepted matches. If you want to only use the incoming accepted
matches, set the Confidence Threshold for a Seed extremely high (like 99999999 or
so). Be careful to accept only high confidence matches prior to using this option, as
any errors in the initial seed set are more likely to propagate.


Main content blockquote


**Related Topics:**


- [Version Tracking Program
Correlators](../VersionTrackingPlugin/VT_Correlators.md)
- [Version Tracking
Wizard](../VersionTrackingPlugin/VT_Wizard.md)
- [Version Tracking Tool](../VersionTrackingPlugin/VT_Tool.md)
- [Version Tracking
Introduction](../VersionTrackingPlugin/Version_Tracking_Intro.md)


---

[← Previous: Program Correlators](../VersionTrackingPlugin/VT_Correlators.md) | [Next: Data Match Correlator →](../VersionTrackingPlugin/VT_Correlators.md)
