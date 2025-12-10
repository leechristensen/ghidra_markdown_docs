[Home](../index.md) > [GhidraGo](index.md) > GhidraGo

# GhidraGo README


## Table of Contents


- [Introduction](#ghidrago-introduction)
  - [Example](#example-of-using-ghidrago-cli)
- [Configure GhidraGo Plugin](#configure-ghidrago-plugin)
- [Configure Protocol Handler (Platform Specific)](#configure-protocol-handler-platform-specific)
  - [Windows](#windows-protocol-handler-configuration)
  - [Linux](#linux-protocol-handler-configuration)
  - [Mac](#mac-protocol-handler-configuration)





## GhidraGo Introduction


GhidraGo is a mechanism to cause Ghidra to display a previously imported program within a
local or multi-user project using a ghidraURL hyperlink similar to an http reference. In
practice ghidraURL's work very similarly to selecting a URL reference which displays a PDF.
Once setup correctly, GhidraURL links can be placed in web pages, external project
documentation files, or any other place a URL hyperlink can be placed.


When a GhidraURL is selected, GhidraGo will startup Ghidra if it isn't already running as
well as prompt to login to the multi-user project if necessary. The program is displayed in
the default tool, usually the codebrowser, and can be configured to re-use an open default
tool or to use a new default tool. The GhidraURL must currently be locating a DomainFile
that is either in a Remote, Shared project, or a local project.


GhidraGo is a combination of a command line program to send a link, a plugin running within
the Ghidra project manager, and the configuration of the default handling for the ghidraURL
within the user environment. The ghidraURL is sent as the first and only parameter to the
ghidraGo command line interface.


GhidraGo passes information through a simple filesystem mechanism vice an open port for
security and simplicity. GhidraGo works on Windows, Linux, and MacOS.


GhidraURL's have the format:


Remote Ghidra Server File:
ghidra://`<host>`[:`<port>`]/&lt;repository-name&gt;/&lt;program-path&gt;
[#&lt;address-or-symbol-ref&gt;]


Example: ghidra://hostname/Repo/notepad.exe#main


Local Ghidra Project File:
ghidra:/[&lt;project-path&gt;/]&lt;project-name&gt;?/&lt;program-path&gt;
[#&lt;address-or-symbol-ref&gt;]


Example: ghidra:/share/MyProject?/notepad.exe#main


### Example of Using ghidraGo CLI


`ghidraGo ghidra://ghidra-server/project/myProgram#symbol`


Executing this command will result in the program called `myProgram` being
opened in Ghidra's default tool with the cursor at `symbol`.


## Configure GhidraGo Plugin


1. Start Ghidra
2. Choose File &gt; Configuration in the Project Window (not the Codebrowser Window)
3. Click the Plug Icon in the upper right to display all plugins
4. Search for GhidraGoPlugin and select it
5. Press OK


Ghidra is now configured to listen to GhidraGo Requests. You can execute a GhidraGo request
using the "ghidraGo" shell/batch script in
`/path/to/ghidra/support/GhidraGo/ghidraGo`


## Configure Protocol Handler (Platform Specific)


Configuring your platform to handle the  protocol is what
enables the ghidraGo command line interface to be associated with a ghidraURL. Once
configured, clicking hyperlinks that start with the  protocol
will execute the ghidraGo CLI with that hyperlink as the first argument. The
configuration is platform specific.


*NOTE: changes to your path to ghidra, such as upgrading ghidra to a new version,
will require the path you set in this configuration to be updated.


### Windows Protocol Handler Configuration


1. Go to Start &gt; Find and Type `regedit`
2. Right click HKEY_CLASSES_ROOT then New &gt; Key
3. Name the key "ghidra"
4. Right Click ghidra &gt; New &gt; String Value and add "URL Protocol" without a value
5. Right Click ghidra &gt; New &gt; Key and create the heiarchy ghidra/shell/open/command
6. Inside command change (Default) to the path where ghidraGo is located followed by
a "%1". For Example:


### Linux Protocol Handler Configuration


In Linux, when you click a browser link with an `href` value to a GhidraURL,
you'll be prompted to use xdg-open.


1. Edit the file `ghidra.desktop` in `~/.local/share/applications`
2. Edit the file mimeapps.list in `~/.local/share/applications`


After the steps above, you should be able to click a GhidraURL href, get the same
xdg-open prompt, and upon clicking "Open xdg-open" GhidraGo should execute and open
Ghidra to the given GhidraURL.


### Mac Protocol Handler Configuration


1. Open `Script Editor` and past the following into the editor.
2. Save the script as an Application named GhidraGo in either
`/Applications` or `~/Applications`
3. Right click on the saved Application and click Show Package Contents
4. Open Contents &gt; Info.plist and under
`<string>com.apple.ScriptEditor.id.GhidraGo</string>`
paste the following:
5. Go to the Applications folder where you saved the GhidraGo, and Open
GhidraGo (run it once).


([Back to Top](#ghidrago-readme))



Last modified: Oct 26 2023


---

[← Previous: Support](../Intro/GhidraSupport.md) | [Next: Headless Analyzer →](../HeadlessAnalyzer/HeadlessAnalyzer.md)
