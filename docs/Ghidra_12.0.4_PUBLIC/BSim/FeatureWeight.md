[Home](../index.md) > [BSim](index.md) > Comparing Feature Vectors

# Features and Weights


## Features of Software Functions


The BSim Database uses a **feature vector**
approach to compare and index software functions. A **feature** is an abstraction that simply means a single element
or attribute that can be compared quantitatively between two objects. The set of possible
features used by a particular approach is fixed, and any object being examined is viewed as
some unordered subset of all the possible features. So features are the smallest (atomic)
aspect of an object that can be measured, either two objects share a feature in common or
they do not. But within this scheme, because objects generally consist of many individual
features, quantitative fine-grained comparisons can be automatically calculated.


The BSim Database extracts its features from the data-flow representation of a function,
after it has been normalized by the Ghidra decompiler. This is the SSA graph representation
of the function, with nodes representing the variables and operators of the function, and
the edges representing the read/write relationships between them. An individual feature is
just a portion of this graph, encompassing some subset of variables and operators and the
specific flow between them. Because of the decompilation, a feature can be viewed naturally
as a uniform snippet of C source code, a partial extraction of some expression in the
source code representation of the function. The full set of features provides uniform (and
overlapping) coverage of the graph representation of the entire function.


Features encode specific aspects of the variables they cover but not others. The size of
a variable, the operator that produced it, and the set of operators it is fed into are
encoded in the features. But, any name assigned to the variable, its data-type, or even its
storage location are *not* encoded in the
features.


Within a function, details about the specific subfunctions that it calls are not encoded
in any of the features for that function, but information describing where the call is made
and the set of parameters it takes is encoded.


## Weighting Software Features


Some features are more useful for identifying a specific function out of a large corpus
than others. With the view that features are just portions of recovered C expressions, some
C expressions are simply more common than others. The BSim Database compensates for these
differences by assigning a weight to each feature that factors in to the similarity and
confidence scores produced when comparing functions. Weighting schemes are considered a
configuration parameter of the database and are established for a particular database when
it is created. The scheme cannot be changed without creating an entirely new database and
reingesting the functions.


Ghidra comes with precomputed weighting schemes that are calculated using statistics
drawn from homogeneous collections of systems and application software. A feature's weight
is computed by counting the number of times it occurs across the entire corpus and
comparing this with the counts from other features. This allows a direct computation of the
information content of the feature; quantitatively, how much have we narrowed down a
particular function from the corpus when we know it contains a particular feature.


The two primary weighting schemes are called **32** and **64**, based
on 32-bit code and one on 64-bit code respectively. This means that a particular database
instance has better sensitivity for either 32-bit or 64-bit functions. The quantitative
scores, similarity and confidence, will be more accurate at distinguishing pairs of
functions from one corpus. This does not mean that functions from the *wrong* group cannot be ingested or queried, but the scores may
not be as accurate. There is also a **64_32**
weighting scheme for architectures where code is compiled to use 64-bit registers but
addresses are still 32-bit.


The specialized weighting scheme **nosize**
allows BSim to match between 32-bit and 64-bit implementations of a function. It works by
making feature hashes blind to the size difference between a 32-bit variable versus a
64-bit variable. This compensates for a compiler's tendency to assign a full 64-bit
register to a 32-bit variable, which is frequently difficult for the decompiler to
automatically resolve in the context of a single function. Because of this blindness, there
is a slight loss of sensitivity, when matching 32-bit to 32-bit functions, or when matching
64-bit to 64-bit, over the **32** or **64** schemes respectively.


The weighting scheme **cpool** should be used for
run-time compilation (JIT) architectures, like Java Dalvik or *.class* byte-code executables. These architectures use
characteristic *constant pool* instructions that delay
exact decisions about code and data layout until runtime. The decompiler can still recover
data-flow effectively by treating these instructions as black-box operations, so BSim works
in the same way as with native code. But a specialized weighting scheme is needed to
balance BSim's sensitivity to these operations.


## Comparing Feature Vectors


For a particular function, the set of extracted features and their assigned weights make
up the formal **feature vector** associated with the
function. When querying a BSim Database, the primary function search is performed by
comparing feature vectors. There are two formal scores that are computed on a pair of
feature vectors, *similarity* and *confidence*.


### Similarity


Similarity is a direct calculation of the percentage of features in common between two
functions. It varies continuously from 0.0, meaning the functions share no features at
all, to 1.0, meaning that the functions have the same feature set. Formally, similarity
is defined as the *cosine similarity* of the two
feature vectors. Weights determine how important individual features are in the score
relative to other features, providing a practical and realistic meaning to the score. Two
functions can exhibit a few unimportant changes, but the similarity can still be very
high because the differences are likely not weighted heavily. Along the same lines, two
functions can share most of their features but have a low similarity because they differ
in more important features.


When searching for a function, the database sets a particular threshold on similarity,
0.7 by default, and returns functions whose similarity with the queried function exceeds
that threshold. This can produce *false positive*
matches for small functions because a small function is described by just a few features
and it is then comparatively easy to randomly match a high percentage of these features.
Deciding if a false positive is likely can be decided quantitatively by examining the
*confidence* score below.


### Confidence


Confidence is a log likelihood ratio, a weighted count of the set of features that
match between two functions minus the set of features that are different. It is an
open-ended score, and the higher it gets, the more likely it is that the two functions
are a true match. Fixing a threshold for the confidence score provides a more consistent
*false positive* rate, as opposed to thresholding on
similarity. A higher score means the two functions have more features in common as an
absolute count, not just a higher percentage. So the chance of randomly matching most of
the features continues to go down as confidence goes up.


A general correspondence between low confidence scores and false positive rates can be
somewhat skewed by *wrappers* and other small
functions, which are always common but whose specific frequency can vary depending on the
type of software. BSim fixes the score 10.0 for a particular wrapper form, providing a
convenient boundary between wrappers and more substantial functions where frequencies are
more consistent. For scores of 10.0 and greater, we get the following rough
correspondence with false positive rate. The rate drops by a factor of 2 for an increase
in confidence of between 4 and 5 points.


> Confidence False Positive Rate
(Approximate) 10 1 in 4,000 26 1 in 100,000 43 1 in 1,000,000 93 1 in 1,000,000,000


For a single function, there is an upper-bound to the confidence that can be achieved
by a possible match, its *self significance*. This
upper-bound is of course reached by comparison with a function having 1.0 similarity.
Self significance is roughly proportional to the size of the function. So its impossible
to achieve a high confidence for a small function, for single matches viewed in
isolation. Of course a medium to low confidence threshold may be enough to produce a
unique match if the database is small, and a medium to high confidence threshold may
still produce occasional false positives even if the database is very large.


---

[← Previous: Weighting Software Features](FeatureWeight.md) | [Next: BSim Feature Visualizer →](../BSimFeatureVisualizerPlugin/BSimFeatureVisualizerPlugin.md)
