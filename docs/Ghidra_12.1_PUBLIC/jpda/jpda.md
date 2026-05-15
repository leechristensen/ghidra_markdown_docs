[Home](../index.md) > [jpda](index.md) > Local

# Debugger Launchers: Java


Our Java Debugger is implemented using the JDK's built-in JPDA/JDI API. We currently have a
mode which embeds it in a `jshell` for CLI-based diagnostics. It is well-suited for Java
and Dalvik (Android VM) targets.


The following launchers based on the Java Debugger are included out of the box:


## Local


The plain "`java`" launcher uses the native Java Debug Interface (JDI) to launch the
current `.class` file locally.


### Setup


You must have Java installed on the local system. No additional setup is required.


### Options


- **Arguments**: These are the command-line arguments to pass into the target.
- **Arch**: The architecture (currently, either "JVM" or "Dalvik").
- **Suspend**: Should the target be suspended on launch.
- **Include virtual threads**: As described.
- **JShell cmd**: If desired, the path to the jshell binary that will host
execution.


## Attach by JDWP


This launcher uses the native Java Debug Interface (JDI) to attach to a running java program
launched with an open Java Debug Wire Port (JDWP) over TCP, e.g.:


-
  ```

  java -agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=localhost:54321 Target.class

  ```


### Setup


Identical to that for the java launcher.


### Options


- **Arch**: The architecture (currently, either "JVM" or "Dalvik").
- **Host**: The host IP where the target is running.
- **Port**: The open JDWP port used by the target.
- **Timeout**: How long to wait for a connection attempt.
- **JShell cmd**: If desired, the path to the jshell binary that will host
execution.


## Attach by PID


This launcher uses the native Java Debug Interface (JDI) to attach to a running java program
launched with a Java Debug Wire Port (JDWP) identified by process id.


### Setup


Identical to that for the java launcher.


### Options


- **Arch**: The architecture (currently, either "JVM" or "Dalvik").
- **Pid**: The target process's ID.
- **Timeout**: How long to wait for a connection attempt.
- **JShell cmd**: If desired, the path to the jshell binary that will host
execution.


---

[← Previous: Attach by JDWP](jpda.md) | [Next: LLDB Integration →](../lldb/lldb.md)
