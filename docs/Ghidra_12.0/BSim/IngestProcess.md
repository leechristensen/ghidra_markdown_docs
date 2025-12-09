[Home](../index.md) > [BSim](index.md) > Migration

# Ingesting Executables


## Ingest
Process


The process of ingesting binaries into a BSim Database server, in order to exploit
Ghidra's data-flow indexing capabilities, can be subdivided into 4 major aspects.


> Importing Executables to a Ghidra Server Analysis Generating Features and Function Metadata Importing Features to a BSim Database


Its possible to populate and use the signature capabilities without putting the binaries
in a Ghidra Server, but it is much easier to generate signatures if step 1 is performed at
some point. Steps 1 and 2 can be performed in either order, or they can be performed
simultaneously. If a Ghidra Server is used, steps 3 and 4 are easily accomplished with the
`bsim` command-line script.


In the following examples, we assume that a machine `localhost` is running both a Ghidra Server and a BSim PostgreSQL database
server. On the Ghidra Server, a repository named `repo` has
been created. On the BSim server, a database named `repo` has
also been created. See [Command-Line Utility Reference](CommandLineReference.md#bsimcommand) for more
details on use of **bsim** command and other supported BSim databases.


### Analysis


Performing Ghidra's normal auto-analysis and ingesting to a Ghidra Server is
accomplished with the `analyzeHeadless` script, designed
explicitly for this purpose.


> $(ROOT)/support/analyzeHeadless
ghidra://localhost/repo -import /path/to/rawexes -preScript
TailoredAnalysis.java


This imports all executables in the directory `/path/to/rawexes` to the repository, running the `TailoredAnalysis` script first and then performing Ghidra's
auto-analysis. Using these pre and post scripts, there is a great deal of flexibility in
how the executables can be analyzed. For a more complete discussion of the available
options, look at the `analyzeHeadlessREADME.txt`.


### Generating Features and Function
Metadata


To generate features and metadata on an existing repository, use the **bsim generatesigs** command. Signatures may be written as
XML files to a local directory and/or committed directly to a specified BSim database. If
not immediately committing to a database and only storing the XML files an appropriate
database configuration may be specified using the *--config* option in lieu of a BSim database URL
(--bsim *`<bsimURL>`*) if database specific executable categories and function tags are not
utilized. Use of the *--config* option does not require a running BSim server.


> $(ROOT)/support/bsim generatesigs
<ghidraURL> </xmldirectory> --config <config_template>
[--overwrite] $(ROOT)/support/bsim generatesigs <ghidraURL> </xmldirectory>
--bsim <bsimURL> [--commit] [--overwrite] $(ROOT)/support/bsim generatesigs <ghidraURL>
--bsim <bsimURL>


Example (generate signature XML files without BSim database commit):


> $(ROOT)/support/bsim generatesigs
ghidra://localhost/repo/folder /xmldirectory
--bsim postgresql://localhost/repo


Example (generate signature XML files and commit to the BSim database):


> $(ROOT)/support/bsim generatesigs
ghidra://localhost/repo/folder /xmldirectory --bsim postgresql://localhost/repo
--commit


Special XML files encoding the metadata are written out to the directory `/xmldirectory`. Every executable indicated by the repository folder
specified by the *ghidraURL* will have metadata generated, one file per
executable, with a file name derived from the MD5 hash of the original executable.
Repository folders will be traversed recursively. The URL can include a specific path
under the repository, in order to select just a portion of the entire repository for
extraction. Output is primarily per function, indicating the functions name, various
attributes, its feature vector, and the list of other functions it calls.


A partially completed **bsim generatesigs**
command can be safely restarted by giving it the same XML directory containing the
partial set of metadata files. Currently it will emit non-fatal warnings for programs in
the repository that were previously processed. You can force it to overwrite the
generated XML files by adding the explicit keyword **--overwrite** as another parameter.


In general, both the Ghidra Server and the BSim server must be running in order for
**bsim generatesigs** command to succeed,
as the BSim server provides configuration information that may be relevant to
the signature generation process, such as database specific executable categories or
function tags.  As in the example above, configuration information
is pulled from the BSim server and signatures are generated from the Ghidra Server
executables. If the **--config**
option is used, assuming the template it specifies is the same one used to create the
database and there are no executable categories or function tags, the BSim server
does not need to be running.


### Importing Features to a BSim
Database


Importing XML signature files into a BSim database which were previously generated is
done using the **bsim commitsigs** command.


> $(ROOT)/support/bsim commitsigs
postgresql://localhost/repo /xmldirectory [--override <ghidraURL> ]


This command takes XML signature files in `/xmldirectory`
and writes the metadata in them to a BSim database, specified by URL. All the executable,
function, and feature vector records are committed to their appropriate tables and all
the indexing is updated if supported. The URL refers to a BSim database rather than a
Ghidra Server and cannot be extended with a path. Any executable paths are already
encoded within the XML file data.


Every executable described within the XML files has a *repository* and *path*
associated with it in the form of a *ghidra://* URL
that was recorded when the XML files were generated. This path can be overridden with the
optional **--override** option where a revised
Ghidra URL may be specified.


The **bsim commitsigs** command can be
safely restarted if an initial run is terminated prematurely. Currently, a restart will
emit a non-fatal warning for each executable that was previously committed.


> **Note:** NOTE: The Ghidra Server used to generate the XML metadata files
does not need to be running for this command to succeed. But, the BSim server must be
running.


## Tailoring
Analysis


It may be necessary as part of the ingest process to alter the way that Ghidra
performs its basic analysis or to add additional steps that gather extra metadata. This
is accomplished by passing a pre-script to the `analyzeHeadless` command. The script is run once for each executable
analyzed, prior to normal analysis. BSim comes with a sample script `TailoredAnalysis.java`, such as:


```

import ghidra.app.script.GhidraScript;
import ghidra.framework.options.Options;
import ghidra.program.model.listing.Program;

public class TailoredAnalysis extends GhidraScript {

        @Override
        public void run() throws Exception {
                Options pl = currentProgram.getOptions(Program.ANALYSIS_PROPERTIES);
                pl.setBoolean("Decompiler Parameter ID", false);
                pl.setBoolean("Stack", false);
        }
}


```


The relevant option group is *Program.ANALYSIS_PROPERTIES*, which contains program specific
properties for all of Ghidra's analysis passes. The example sets the specific options,
"Decompiler Parameter ID" and "Stack", to false, which causes Ghidra to skip those
passes. Other passes can be toggled or have their parameters altered in this way, see [“Analysis Effects on Feature
Extraction”](IngestProcess.md#analysiseffects) for some of analysis passes that can effect BSim.


### Ingesting Executable Categories


If the BSim database has been tailored to ingest special *executable categories*, the extra metadata associated with an
executable must be explicitly calculated and stored on the formal Ghidra program in
order for BSim to see it. This is also accomplished with a Ghidra script passed to
*analyzeHeadless*. BSim expects to find specific
category values stored as Ghidra program options under *Program.PROGRAM_INFO*. A value can be set by passing the
category name and the value itself as strings to the *setString* method on the *Options* object. The following example sets values for the
category "WebResource".


```

@Override
public void run() throws Exception {
        Options pl = currentProgram.getOptions(Program.PROGRAM_INFO);
            String value = discoverWebResource();
            String value1 = discoverAnotherWebResource();
            Date compiledate = lookupCompileDate();
            pl.setString("WebResource",value);
            pl.setString("WebResource_1",value1);
            pl.setDate("Compile Date",compiledate);
}

```


The script has all the responsibility for constructing any actual value, and it can
be run either as a pre-script or a post-script. Thus it can use the results of Ghidra's
basic analysis to calculate the value or retrieve it from some external source like a
CSV file. Once the script sets the value, assuming the executable category has already
been added to the BSim database instance, there are no additional steps to take, and
the rest of the BSim ingest process will make sure the value is incorporated into the
database.


If more than one value needs to be assigned to the same category, the script must
assign the first value to the option matching the category name and then assign
additional options with names obtained by appending '_1', '_2', and so on to the
category name. For the executable time-stamp, BSim reads the option matching the name
of the specific *Date* executable category. This
can be set within a script by using the *setDate*
method instead of *setString*. If no *Date* category has been created, BSim will read the 'Date
Created' option, which is normally filled in with the time at which Ghidra was created
and analysis started. For additional discussion see [“Executable
Categories”](DatabaseConfiguration.md#execat).


### Ingesting Function Tags


If a set of *function tags* have been
registered with the BSim database, some form of analysis must still place the tags on
individual functions in a Ghidra program. As with executable categories, this can be
accomplished with a Ghidra script passed to *analyzeHeadless*. Once a set of functions is identified, the
tag(s) can be added using methods on the standard *Function* object. This script snippet looks up the function
object by address and then sets the *LOGGING* tag
on it and removes the *SERIALPORT* tag.


```

public void adjustTags(Address myaddress) throws Exception {
        Function func = program.getFunctionManager().getFunctionAt(myaddress);
        func.addTag("LOGGING");
        func.removeTag("SERIALPORT");
}

```


If the tag did not exist before the first call to *addTag*, it will be created. Assuming the tag has been
registered with BSim, it will now automatically be included as part of the metadata of
any functions it was added to. For additional discussion see [“Function
Tags”](DatabaseConfiguration.md#functiontags).


## Analysis
Effects on Feature Extraction


Auto-analysis *must* be performed in some form,
in order to perform disassembly and identify functions, before features can be generated.
Only code that has been formally identified as a function by Ghidra will have its
features extracted and ingested by the successive steps. The single most important driver
of success for future queries finding an executable is the amount of functions that have
been formally identified by analysis. For most common file formats and architectures,
Ghidra's default settings will provide good coverage, but depending on the type of
executable data, it may be necessary to provide additional scripts to the analysis
process.


Ghidra has numerous **Analyzers**, that can be
turned on or off during ingest. Many of these can affect code coverage and should be left
*on* be default. A small number of settings, on
Analyzers or elsewhere, can actually change which features are extracted for a function,
even though code coverage is unaffected. The rule of thumb is that, among those settings
that can affect features, the settings used during ingest should also be the same
settings used by the end-user when they are analyzing an unknown binary and querying
against the database. In most cases, the best approach is to use the default settings for
both ingest and query, but if you make a change, be sure to make it on both sides. A
difference in settings may not completely prevent successful queries, but is likely to
introduce some amount of noise.


Analyzers which can affect features include:


> Call-Fixup
Installer This controls how the decompiler works with prologue, epilogue, and other
special compiler bookkeeping functions. There is little reason to turn this
off. Decompiler Parameter
ID This does a global analysis of how individual functions are passing parameters
which may affect the features for some functions, although in most cases the
effect will be small. Currently it's safest to turn this off. Known Functions That Do No
Return This identifies certain common functions that do not return to the caller.
This can have a limited effect on features of functions that call these routines.
There is little reason to turn this off. Shared Return
Calls This identifies common compiler optimizations where a subfunction is accessed
via a jump instruction rather than a call . Misidentifying these
instructions can have a big effect on extracted features. There are only a
limited set of circumstances where it makes sense to turn this Analyzer off.


Scripts can be used to alter settings on any number of objects during the analysis
process. A few of these can have significant impact on extracted features. With the
exception of symbol names and data-types, which *do
not* have an effect on features, anything that changes decompilation will
likely change the extracted features. These settings include:


> Call-Fixup , Inline , No Return Toggling these settings in a function prototype will affect the features of
any calling function. Read-only
Settings Memory blocks or individual data items can be marked as read-only , causing the decompiler to propagate the
underlying value as a constant. Register
Settings Its possible to mark registers as holding specific values for specific
functions. The decompiler will respect this and likely propagate the
constant.


## Maintenance


The **bsim** script provides a minimal number
of maintenance commands for a BSim server, described below. For a PostgreSQL server, it
is possible to use the bundled SQL command line tool
**psql** in order to make changes directly to
the tables. But for very large modifications to the database, the best option may be to
recreate the database, which is slightly less onerous than it sounds. The most CPU
intensive part of the ingest process, Ghidra's auto-analysis, typically does not need to
be rerun across everything. Regenerating the metadata files and reimporting takes much
less time. Additional efficiency may be gained by dropping and then regenerating the main
index after (re)ingesting. (See below)


### Deleting Executables


The database currently cannot remove individual function records. The records for an
entire executable, and all the functions associated with it, can be removed. To remove
an executable, use one of the following forms of the delete command:


> $(ROOT)/support/bsim delete <bsimURL> --md5 7abf... $(ROOT)/support/bsim delete <bsimURL> --name ...


In the *--md5* form, you specify the 32 character
hex representation of the md5 hash of the executable, which should identify it
uniquely. Using the *--name* form, there is the
possibility that the name is not unique, in which case the command will fail.


If a unique executable is identified, its metadata record will be removed, and the
records for all functions which that executable formally contains will also be removed.
For deployments which also maintain a loosely coupled Ghidra Server, keep in mind that
removing executables from the BSim database with these commands does not remove the
corresponding program from the Ghidra Server, this requires an additional step.


### Updating Names and Other Metadata


It is feasible to delete an executable from the database and then reingest it in
order to populate updated information into the database, but this is fairly inefficient
because you need to reperform all the function decompilation. Additionally this causes
a large rearrangement of the database tables in order to perform what may amount to a
very small change. The BSim database supports an *update* operation designed to make in-place changes to the
metadata describing executables and functions. This is primarily useful for
synchronizing function names with the BSim database as analysts rename them and commit
their changes to a Ghidra Server, however other metadata, like executable architecture
or category properties, can also be changed.


Very similar to the two ingest commands, **generatesigs** and **commitsigs**, there are also two update commands **generateupdates** and **commitupdates** which are invoked as follows:


> $(ROOT)/support/bsim generateupdates
<ghidraURL> </xmldirectory> --config <config_template>
[--overwrite] $(ROOT)/support/bsim generateupdates <ghidraURL> </xmldirectory>
--bsim <bsimURL> [--commit] [--overwrite] $(ROOT)/support/bsim generateupdates <ghidraURL> --bsim <bsimURL> $(ROOT)/support/bsim commitupdates <bsimURL>
</xmldirectory>


The **generateupdates** command produces
stripped down metadata XML files for every executable contained within the repository
folder specified by the *ghidraURL*. Just like the **generatesigs** command, it can take an optional **--config *&lt;config_template&gt;*** parameter, which
allows the command to execute without the BSim server running, otherwise a **--bsim *`<bsimURL>`***
parameter is required. It can also take an
optional **--overwrite** parameter, causing it
to overwrite any previously generated XML files. If the
**--bsim** option is specified with the **--commit**
option updates will be committed directly to the database. A BSim database commit is
always performed using the specified *bsimURL* if an *xmldirectory* is
not specified.


The **commitupdates** command commits the
generated metadata to the BSim server. Only the smallest required change is issued as a
formal transaction to the database, and the number of changes that are actually made
are reported per executable. Functions and executables cannot be added or deleted to
the BSim database using this command. If the update file describes new functions in a
preexisting executable, this command will issue warnings about the existence of the new
functions but will not create function records. Other functions will still get
updated.


### Dropping the Feature Vector Index


**NOTE:** Applies to PostgreSQL or Elasticsearch databases only


For those users performing large ingests or who find themselves rebuilding the
database frequently, it is possible to drop the main index, ingest data, then recreate
the main index. This is likely to be faster overall than the default behavior of
updating the index as data is ingested. To drop the index, use the command:


> $(ROOT)/support/bsim dropindex <bsimURL>


Once the data has been ingested, rebuild the index with the command:


> $(ROOT)/support/bsim rebuildindex <bsimURL>


The time it takes to rebuild depends directly on the number of functions that have
been ingested. For very large collections, rebuilding can take hours or days. The
database can still be accessed while the index is dropped, but queries may take
much longer to complete.


### Prewarming the Database


**NOTE:** Applies to PostgreSQL databases only


A maintainer can issue the **bsim
prewarm** command to prepopulate RAM with commonly accessed portions of a
BSim database.


> $(ROOT)/support/bsim prewarm
ghidra://localhost/repo


Without this command, initial queries to a *cold* database (one that has just been restarted) can run
slowly, giving poor response times until the cache is fully populated. A query
typically needs to access an effectively random subset of pages making it a bad method
for refreshing the cache.


The command is intended to be run once, immediately after restarting a server and
before any queries have been made. It attempts to quickly preload the main vector
index, and possibly portions of other tables, into RAM, by reading from disk
sequentially. Queries may continue to improve as the database optimizes its cache
across all tables, but the command effectively eliminates slow initial queries.


## Migration


BSim is a prototype capability, and the database layout may be subject to change. We
intend to minimize the impact of this to the extent possible, and in particular, major
changes should be limited to major Ghidra releases. But its possible in general that an
existing BSim database will be incompatible with both the client and server from a new
release.


Unfortunately, the only option to upgrade in these cases is to reingest the executables
into a new BSim database. Frequently the first two stages of ingest (See [*Ingesting
Executables*](IngestProcess.md)), importing executables to a Ghidra Server and running auto-analysis,
do not need to be repeated. Only the final two stages need to be performed, generating
and importing features to the BSim server, usually accomplished with the *generatesigs* and *commitsigs* commands.


BSim fundamentally depends on the Ghidra decompiler, which steadily adds new analysis
features that can affect compatibility over time. Many additions have no effect on BSim,
have a small effect, or affect only a tiny percentage of functions. To minimize the
impact to existing databases, the decompiler, independent of the Ghidra release, is
assigned a *major* and *minor* version number. A change in the minor number of 1 or 2
should have little to no impact for most queries, but users will have to tolerate this
rare degradation of results if they place queries using a client that doesn't match the
BSim server's version. If the client and server differ by a major version, queries will
return an error message.


---

[← Previous: Maintenance](IngestProcess.md) | [Next: Features and Weights →](FeatureWeight.md)
