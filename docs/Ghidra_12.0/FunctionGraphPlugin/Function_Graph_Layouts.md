[Home](../index.md) > [FunctionGraphPlugin](index.md) > Layouts

# Function Graph Layouts


## Nested Code Layout


The nested code layout use the
<a name="helptopicsdecompileplugindecompilerhtm"></a>Decompiler to arrange the
code blocks of a function in a way that mimics the nesting of the source code as seen
in the decompiled function.   As an example, any code block that must pass through an
`if` statement will be nested below and to the right of the code block that
contains the conditional check.   The nested code block is **dominated** by the block
containing the conditional check--code flow can only reach the nested block by passing
through the block above it.   Also, code blocks that represent a default code flow
will be aligned to the left and below other code blocks in the function.   This layout
allows the user to quickly see the dominating relationships between code blocks.


The edges leaving a code block are labeled with the type of high-level conditional
statement (e.g., `if`, `if/else`, etc) used to determine code flow.


By default, edges are routed such that they are grouped together such that any edges
returning to a shared code block will overlap.  This reduces visual clutter at the
expense of being able to visually follow individual edges to their vertices.  Another
consequence of this routing is that sometimes edges will travel behind unrelated
vertices, again, making it difficult to visually follow these edges.  The edge
routing can be changed via the options below.


### Nested Code Layout Options


The **Route Edges Around Vertices** option triggers this layout to route
edges around any vertex that would otherwise touch that edge.  (See above for
notes on how edges are routed for this layout.)


The **Use Dim Return Edges** option makes default code block return flow edges
lighter than conditional edges.  This makes it easier for users to scan the
graph and ignore return flows.


## Flow Chart Layout


This layout organizes the code blocks into a tree structure with each parent vertex in the
tree being centered over its children. Edges are routed orthongally with minimal edge
crossings.


## Flow Chart Layout (Left)


This layout is the same as the Flow Chart Layout, except parent nodes are place directly
above their left most child.


*Provided by: *Function Graph Plugin**


---

[← Previous: Zooming](Function_Graph.md) | [Next: Program Graph →](../ProgramGraphPlugin/ProgramGraph.md)
