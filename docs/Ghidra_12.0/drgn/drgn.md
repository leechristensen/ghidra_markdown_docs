[Home](../index.md) > [drgn](index.md) > Linux Kernel

# Debugger Launchers: drgn


The following launchers uses Meta's **drgn** engine to explore various targets:


## Attach


The "`drgn`" launcher attaches to a running process via the Linux "/proc/pid"
interface.


### Setup


You must have Meta's **drgn** installed on the local system. The default behavior assumes
you do NOT need root access to attach to a running process, i.e. it assumes you have run the
command:


-
  ```

  echo 0 > /proc/sys/kernel/yama/ptrace_scope

  ```


using root privileges at some point. Alternately, you can prepend "sudo -E" to the drgn
invocation line in "local-drgn.sh"". Note: **drgn** does not currently support stack
unwinding or register access for user-mode access to running processes.


### Options


- **PID**: The running process's id


## Core Dump


This launcher loads a Linux core dump.


### Setup


You must have Meta's **drgn** installed on the local system. No other setup is required.
Note: Core dumps may or may not include memory, so the Dynamic Listing may or may not be
populated.


### Options


- **Core dump**: The core-dump file


## Linux Kernel


This launcher attaches to a Linux kernel via the "/proc/kcore" interface.


### Setup


You must have Meta's **drgn** installed on the local system. No other setup is required.
Note: requires root access - you will be prompted for a password in the Terminal.


### Options


- **None**


---

[← Previous: Core Dump](drgn.md) | [Next: Connection Manager →](../TraceRmiConnectionManagerPlugin/TraceRmiConnectionManagerPlugin.md)
