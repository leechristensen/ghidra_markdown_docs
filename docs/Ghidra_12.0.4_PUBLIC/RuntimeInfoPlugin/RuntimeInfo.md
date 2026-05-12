<a name="runtimeinfo"></a>


# Runtime Information


The Runtime Information feature pops up a dialog showing information about the internal
settings of the active Ghidra installation. It is primarily a diagnostic tool to aid in
debugging.


To display the Runtime Information dialog:


- From the Project Window, Select **Help →
Runtime Information** from the menu.


Runtime Information categories are organized in tabs. The following categories are provided:


- **Version** - Ghidra, Operating System, and Java version information. Clicking the
***Copy*** button will copy this information to the clipboard for easy transfer into a bug report.
- **Memory** - JVM memory usage.  Clicking the ***Collect Garbage*** button will
suggest to the JVM that garbage collection should run.
- **Application Layout** - Ghidra application layout information, including directory
locations.
- **Properties** - Defined JVM system properties for the active Ghidra application.
- **Environment** - Defined environment variables for the active Ghidra application.
- **Modules** - A list of discovered Ghidra Modules.
- **Extension Points** - A list of discovered Ghidra Extension Points.
- **Classpath** - The ordered classpath for the active Ghidra application.
- **Extensions Classpath** - The ordered extensions classpath, if the
***ghidra.extensions.classpath.restricted*** property is set (see
*support/launch.properties*).
