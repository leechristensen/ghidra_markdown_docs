[Home](../index.md) > [DebuggerPlatformPlugin](index.md) > Platform Selection

# Debugger: Platform Selection


The Debugger allows the user to work with multiple platforms, i.e., architectures,
compilers, etc., within the context of a single debug target. This plugin facilitates switching
among platforms and introducing new platforms.


Note we are currently supporting two trace database conventions. In the first, the system
ascertains the target's platform and maps it to a Ghidra language and compiler spec at the time
the trace is created. These are called the *base* language and base compiler spec.
Together, they comprise the trace's *host platform*. This is used by "Recorder-mode"
traces and most "TraceRmi-mode" traces.


However, there are some cases where it is impractical to know the platform before creating
the trace, e.g., when setting up "raw" connections. For these cases we have a second
convention: The system creates a trace with the host platform
`DATA:BE:64:default:pointer64`, for example. Thus, disassembly requires the system
(or user) to ascertain the platform at a later time. This can then be mapped into the existing
trace as a *guest platform*. Either convention permits guest platforms, but they are a
necessary aspect of the second. If the system has failed to ascertain the platform, the user
may attempt to do so by adding *override* platforms in trial-and-error fashion.
Furthermore, even if the system has succeeded, there may be cause to try disassembly in
alternative languages, e.g., Java bytecode when debugging its x86 JVM at the native level.


## Actions


This plugin adds actions under the **Debugger → Choose Platform** menu.


### Host/base


This action corresponds to the current trace's host platform. Technically, this is just one
platform option among possible recommendations, but it is always among them. If the host
language is **DATA:...**, then this platform will not support disassembly. A guest platform
is necessary.


### *[Platform Name]*


This action is replicated for each recommended platform and for each platform already
present in the trace. The recommendations are given by an opinion service, so new options may
be added by Ghidra extension modules. It is possible there are no recommendations for the
current trace. The current platform is indicated by a check mark.


### More...


This action is enabled whenever there is a current trace. It presents a dialog with the
recommended platforms for the trace.


![](images/DebuggerSelectPlatformOfferDialog.png)


The "Show Only Recommended Offers" check can be disabled to display *override*
platforms as well. Every language-compiler-spec pair is offered as an override platform.
Selecting an offer and confirming the dialog will add or change to the selected platform in the
trace. Furthermore, the choice will be added to the **Choose Platform** menu for the current
trace.


---

[← Previous: Comparing Times](../DebuggerTraceViewDiffPlugin/DebuggerTraceViewDiffPlugin.md) | [Next: Decompiler →](../DecompilePlugin/DecompilerIntro.md)
