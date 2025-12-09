[Home](../index.md) > [HeadlessAnalyzer](index.md) > Headless Analyzer

# Headless Analyzer


The *Headless Analyzer* is a command-line-based (non-GUI) version of Ghidra that allows users to:


- Create and populate projects
- Perform analysis on imported or existing binaries
- Run non-GUI scripts in a project (scripts may be program-dependent or program-independent)


The Headless Analyzer can be useful when performing repetitive tasks on a project (i.e., importing and analyzing a directory of files or running a script over all binaries).


## **Headless Analyzer Options**


The following options are available for the Headless Analyzer:


analyzeHeadless [&lt;project_location&gt; &lt;project_name&gt;[/&lt;folder_path&gt;]] **|**

[ghidra://`<server>`[:`<port>`]/&lt;repository_name&gt;[/&lt;folder_path&gt;]]



[[-import [`<directory>`|`<file>`]+] | [-process [&lt;project_file&gt;]]]

[-preScript `<ScriptName>` [`<arg>`]*]

[-postScript `<ScriptName>` [`<arg>`]*]

[-scriptPath "`<path1>`[;`<path2>`...]"]

[-propertiesPath "`<path1>`[;`<path2>`...]"]

[-scriptlog `<path to script log file>`]

[-log `<path to log file>`]

[-overwrite]

[-recursive [`<depth>`]]

[-readOnly]

[-deleteProject]

[-noanalysis]

[-processor `<languageID>`]

[-cspec `<compilerSpecID>`]

[-analysisTimeoutPerFile `<timeout in seconds>`]

[-keystore `<KeystorePath>`]

[-connect [`<userID>`]]

[-p]

[-commit ["`<comment>`"]]

[-okToDelete]

[-max-cpu `<max cpu cores to use>`]

[-librarySearchPaths `<path1>`[;`<path2>`...]]

[-loader `<desired loader name>`]


## **Accessing the Headless Analyzer**


- The shell script that launches the Headless Analyzer can be found in your Ghidra installation's *support* folder.
- Execute the *analyzeHeadless* shell script from the command line with the desired options.


## **Headless Analyzer Documentation**


- The *analyzeHeadlessREADME.html* file contains details on Headless Analyzer usage and options. It is located in your Ghidra installation's *support* folder.


---

[← Previous: GhidraGo](../GhidraGo/GhidraGo.md) | [Next: Keyboard Navigation →](../KeyboardNavigation/KeyboardNavigation.md)
