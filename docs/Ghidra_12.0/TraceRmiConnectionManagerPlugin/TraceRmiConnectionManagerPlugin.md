[Home](../index.md) > [TraceRmiConnectionManagerPlugin](index.md) > Connection Manager

# Debugger: Connections


![](images/TraceRmiConnectionManagerPlugin.png)


The Connections window manages connections to live debuggers and, at a high level, their
targets. Each item is a Trace RMI connection (or a step toward one) to a back-end debugger.
Usually, the back end is a native debugger with a plugin that communicates with Ghidra via
Trace RMI. These connections are typically established using a launcher script, invoked from
the [Launcher
Menu](../TraceRmiLauncherServicePlugin/TraceRmiLauncherServicePlugin.md), though there are actions here for establishing connections manually or to remote back
ends. There are different kinds of items displayed in the connection list.


- ![Thread](../icons/thread.png) **Server:** This node displays the current
state of the Trace RMI server. Ordinarily, the server is not used, since Ghidra can accept
connections on a one-off basis without starting a persistent server. Nevertheless, often for
development purposes, it may be convenient to keep a socket open. There is only one server,
and it is either listening on a port, or not.
- ![Accept](../icons/connect-accept.png) **Acceptor:** Each acceptor is ready
to receive a single connection from a Trace RMI client. The node displays the host/interface
and port on which it is listening. Once it has received a connection, the acceptor is
destroyed.
- ![Connect](../icons/connect.png) **Connection:** A connection is a complete
connection to a Trace RMI client. It may have one or more (but usually only one) target trace
associated with it. The node displays a description given by the client along with the remote
host and port. Double-clicking the node will expand its targets, if any. If the connection is
updating any trace, a busy ovelay is displayed on the icon.
- ![Record](../icons/record.png) **Target:** These are children of their
creating connection. A client can create any number of traces to describe each target it
wishes to trace, but by convention each client ought to create only one. The target node
displays the name of the trace and the last snapshot activated by the client. Double-clicking
the node will activate the target at the last snapshot, and change to **Control Target**
[mode](../DebuggerControlPlugin/DebuggerControlPlugin.md#control-mode).
If the connection is updating this target's trace, a busy overlay is displayed on the
icon.


## Actions


### Connect Outbound ![Outbound](../icons/connect-outbound.png)


Connect to a back end. The back end plays the role of TCP server while Ghidra plays the TCP
client. The dialog prompts for the (possibly remote) back end's host and port. Once the
connection is established, the back end takes the role of Trace RMI client, despite being the
TCP server. Check the command documentation for your back end's plugin to figure out how to
have it listen first.


![](images/ConnectDialog.png)


### Connect by Accept ![Accept](../icons/connect-accept.png)


Accept a single connection from a back end. Ghidra plays the role of TCP server, and the
back end is the TCP client. The dialog prompts for the host/interface and port on which to
listen. Check the command documentation for your back end's plugin to figure out how to have it
connect to a listening Ghidra. Once the connection is established, the listening port is
closed. The back end plays the role of Trace RMI client.


### Close


Right-click a connection or acceptor to access this action. For an acceptor, this will
cancel it. For an established connection, this will tear it down, rendering its target traces
dead. Note that the back end may retain its live targets, despite losing its connection to
Ghidra.


### Close All


Burn it all to the ground and start over. This closes the server, cancels all acceptors, and
tears down all connections. Any live trace in the Debugger will be rendered dead, which often
causes the trace manager to close them. Note that the back ends may retain their live targets,
despite losting their connections to Ghidra.


### Start Server


Start a persistent server, able to accept many back-end connections. Ghidra plays the role
of TCP server, and each back end is a TCP client. The dialog prompts for the host/interface and
port on which to listen. Check the command documentation for your back end's plugin to figure
out how to have it connect to a listening Ghidra. The listening port remains open no matter how
many connections it has accepted. It is still possible to connect by other means while the
server is active.


### Stop Server


Stop the server. This closes the persistent server. This does not affect pending acceptors
or established connections.


### Forcibly Close Transactions


Forcibly close all the back-end's transactions on the target trace. This is generally not a
recommended course of action, except that sometimes the back-end crashes and fails to close a
transaction. Un-closed transactions from the back-end can leave most, if not all, of the UI in
a stale state, since event processing on the trace is disabled. If there is good reason to
believe the back-end has forgotten to close a transaction, this action will forcibly close all
of them and re-enable event processing. If, however, the back-end was in fact still doing work
with that transaction, it may crash and/or corrupt the connection.


---

[← Previous: Linux Kernel](../drgn/drgn.md) | [Next: Troubleshooting →](../Debugger/Troubleshooting.md)
