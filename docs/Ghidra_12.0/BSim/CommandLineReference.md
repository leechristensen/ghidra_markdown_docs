[Home](../index.md) > [BSim](index.md) > BSim Command (bsim)

# Command-Line Utility Reference


## `bsim_ctl`


```

    bsim_ctl start           </datadir-path> [--auth|-a pki|password|trust] [--noLocalAuth] [--cafile </cacert-path>] [--dn "<distinguished-name>"]
    bsim_ctl stop            </datadir-path> [--force]
    bsim_ctl status          </datadir-path>
    bsim_ctl adduser         </datadir-path> <username> [--dn "<distinguished-name>"]
    bsim_ctl dropuser        </datadir-path> <username>
    bsim_ctl resetpassword   <username>
    bsim_ctl changeauth      </datadir-path> [--auth|-a pki|password|trust] [--noLocalAuth] [--cafile </cacert-path>] [--dn "<distinguished-name>"]
    bsim_ctl changeprivilege <username> admin|user

    Global Options:
        --port|-p <portnum>
        --user|-u <username>
        --cert </certfile-path>

```


**bsim_ctl** is a command-line utility for
starting and stopping a BSim server using the PostgreSQL back-end. The utility cannot be
used with either an Elasticsearch server or a local H2 database.
All commands must be run on the machine hosting the server.
Optional parameters for a given command are indicated by square brackets '[' and ']'
and always start with either '-' or '--' characters.  If an associated value is required
and contains space characters it should be enclosed in double quotes.  Options which require
a value may be separated by a space or a equal "=" character (e.g.,
**--auth=password**).




**start**


Initializes and starts a PostgreSQL server. The command-line must include a path
to the data directory for the server, which must exist. If a server had run
previously and populated this directory, this command simply restarts the server
using the preexisting data and configuration; otherwise, a new database is
initialized. The user performing the initial start is automatically added to the
database with *admin* privileges.


During a restart, any authentication options (with the exception of the global
**--cert** option) are unnecessary and will
be ignored. The PostgreSQL server will be restarted with the already established
settings. To actually change the settings, use the **changeauth** command before restarting.


**--auth|-a***`<type>`* - specifies the authentication type (**pki |
password | trust**) for a new database: *trust* for no authentication, *password* for password authentication, and *pki* for authentication using public key certificates.
With the *pki* setting, both the **--cafile** and the **--dn** options also need to be provided; additionally
the **--cert** option must be provided unless
the **--noLocalAuth** option is also
given.


**--noLocalAuth** - used together with
the **--auth** option causes
authentication to not be required for local connections, i.e. localhost.


**--cafile***&lt;/cafile-path&gt;* - specifies an absolute path to a
certificate authority file and is required for **--auth pki**. This file should contain the
certificates the PostgreSQL server will use to authenticate in PEM format
concatenated together.


**--dn***&lt;distinguished-name&gt;* - specifies the Distinguished
Name for the admin user and is required for
**--auth pki**.


**--port|-p***`<portnum>`* - specifies the port the PostgreSQL server will
listen on. For port numbers other than the default 5432, URLs and other
command-lines must explicitly specify the port, when connecting to the server. This
option only effects the initial start of a server. For subsequent (re)starts this
option is ignored, and the server will continue to listen on the same port
specified in the initial start. Use **changeauth** to change the port of a server after
its initial start.


**stop**


Stops a currently running PostgreSQL server. The path to the actively used data
directory must be provided. By default, shutdown will wait until existing
connections to the database have been closed.


**--force** - causes existing
connections to be forcibly closed and the PostgreSQL server to shut down
immediately.


**status**


Retrieves the status of a PostgreSQL server (running/down). The path to the
actively used data directory must be provided.


**adduser**


Give a new user permission to access the PostgreSQL server. The path to the
actively used data directory and a single username must be specified. The server
must be running. New users are given *user*
(read-only) privileges, unless a subsequent **changeprivilege** command is used.


**--dn***&lt;distinguished-name&gt;* - specifies the Distinguished Name of the new user,
which is required if the database enabled **--auth pki**. This option can be used to provide a
Distinguished Name to a preexisting user, if the PostgreSQL server's authentication
strategy is changed.


**dropuser**


Remove access to the PostgreSQL server for a specific user. The path to the
actively used data directory and a single username must be specified. The server
must be running.


**changeauth**


Change the configuration of a previously initialized PostgreSQL server. The path
to the server's data directory must be specified. The server must not currently be
running to use this command, which only takes effect after a restart. Options have
the same meaning as for the **start**
command.


**--port|-p***`<portnum>`* - changes the port the PostgreSQL server will
listen on. If this option is not present, the server will continue to listen on the
same port.


**--auth|-a***`<type>`* - changes the authentication type (**pki |
password | trust**) used by the PostgreSQL server. No change is made if the
option is not present. If the option is present, omitting the **--noLocalAuth** causes local connections to require
authentication. This command does not affect the presence or absence of passwords
or Distinguished Names for existing users.


**--cafile***&lt;/cafile-path&gt;* - specifies an absolute path to a
certificate authority file and is required for **--auth pki**. This file should contain the
certificates the PostgreSQL server will use to authenticate in PEM format
concatenated together.


**--dn***&lt;distinguished-name&gt;* - specifies the Distinguished Name for the admin
user and is required for **--auth pki**.


**resetpassword**


Reset the password for a user. A single user must be specified, and the
PostgreSQL server must be running. The password will be reset to 'changeme'.


**changeprivilege**


Change access privilege for a user. A single user must be specified followed by
**admin** or **user**, and the PostgreSQL server must be
running.


**--Global
Options--**


These options apply to all the **bsim_ctl** commands that connect to an active
PostgreSQL server: **start**, **adduser**, **dropuser**, **resetpassword**, and **changeprivilege**.


**--port|-p***`<portnum>`* - specifies the port on which to connect with
the PostgreSQL server.


**--user|-u***`<username>`* - specifies a user name to use when connecting
to the PostgreSQL server.


**--cert***&lt;/certfile-path&gt;* - provides the absolute file path to the
user's certificate when connecting to a PostgreSQL server that requires PKI
authentication.


## `bsim`


```

    bsim createdatabase  <bsimURL> <config_template> [--name|-n "<name>"] [--owner|-o "<owner>"] [--description|-d "<text>"] [--nocallgraph]
    bsim setmetadata     <bsimURL> [--name|-n "<name>"] [--owner|-o "<owner>"] [--description|-d "<text>"]
    bsim getmetadata     <bsimURL>
    bsim addexecategory  <bsimURL> <category_name> [--date]
    bsim addfunctiontag  <bsimURL> <tag_name>
    bsim dropindex       <bsimURL>
    bsim rebuildindex    <bsimURL>
    bsim prewarm         <bsimURL>
    bsim generatesigs    <ghidraURL> </xmldirectory> --config|-c <config_template> [--overwrite]
    bsim generatesigs    <ghidraURL> </xmldirectory> --bsim|-b <bsimURL> [--commit] [--overwrite]
    bsim generatesigs    <ghidraURL> --bsim|-b <bsimURL>
    bsim commitsigs      <bsimURL> </xmldirectory> [--md5|-m <hash>] [--override <ghidraURL>]
    bsim generateupdates <ghidraURL> </xmldirectory> --config|-c <config_template> [--overwrite]
    bsim generateupdates <ghidraURL> </xmldirectory> --bsim|-b <bsimURL> [--commit] [--overwrite]
    bsim generateupdates <ghidraURL> --bsim|-b <bsimURL>
    bsim commitupdates   <bsimURL> </xmldirectory>
    bsim listexes        <bsimURL> [--md5|-m <hash>] [--name|-n <exe_name>] [--arch|-a <languageID>] [--compiler <cspecID>] [--sortcol|-s md5|name] [--limit|-l <exe_count>] [--includelibs]
    bsim getexecount     <bsimURL> [--md5|-m <hash>] [--name|-n <exe_name>] [--arch|-a <languageID>] [--compiler <cspecID>] [--includelibs]
    bsim delete          <bsimURL> [--md5|-m <hash>] [--name|-n <exe_name> [--arch|-a <languageID>] [--compiler <cspecID>]]
    bsim listfuncs       <bsimURL> [--md5|-m <hash>] [--name|-n <exe_name> [--arch|-a <languageID>] [--compiler <cspecID>]] [--printselfsig] [--callgraph] [--printjustexe] [--maxfunc <max_count>]
    bsim dumpsigs        <bsimURL> </xmldirectory> [--md5|-m <hash>] [--name|-n <exe_name> [--arch|-a <languageID>] [--compiler <cspecID>]]

    Global options:
        --user|-u <username>
        --cert <certfile-path>

```


See [“Ghidra and BSim
URLs”](CommandLineReference.md#ghidra-and-bsim-urls) below for details about specifying *ghidraURL* and *bsimURL*
properly. See [“Database
Configuration”](DatabaseConfiguration.md) for guidance on the various BSim Databases which are
supported.


**bsim** is a command-line utility for
managing the generation and ingest of BSim signatures and metadata. Depending on the
subcommand, it connects to a Ghidra Server and/or a BSim database server. A *ghidraURL* refers to Ghidra Server or local project using the
**ghidra:** protocol, while *bsimURL* refers to a BSim database server with the appropriate
**postgresql:**, **https:**, or **file:** protocol specified. The **elastic:** protocol is equivalent to and may be used in
place of the **https:** protocol.
Optional parameters for a given command are indicated by square brackets '[' and ']'
and always start with either '-' or '--' characters.  If an associated value is required
and contains space characters it should be enclosed in double quotes.  Options which require
a value may be separated by a space or a equal "=" character (e.g.,
**--name=myname**).


**createdatabase**


Creates a new empty repository. A URL and configuration template (**config_template**) is required. The new database name
is taken from the path element of the URL.  See [“Creating a
Database”](DatabaseConfiguration.md#creating-a-database) for more details and discussion on configuration template use.
See [“Creating Database Templates“](DatabaseConfiguration.md#creating-database-templates)
if a standard template will not suffice.


Supported configuration templates (**config_template**) are defined within the Ghidra
installation in XML form. The following configurations are currently defined:
(**large_32, medium_32, medium_64, medium_cpool,
medium_nosize**).


**--name|-n** - specifies a formal, more
descriptive, name for the repository that can be used for the BSim client
display.


**--owner|-o** - gives a descriptive name
for the owner of the repository and/or the data it will contain.


**--description|-d** - specifies a short
string describing the intended contents of the new repository.


**--nocallgraph** - disables storing call
relationships between ingested functions. Default is to store call relationships.


**setmetadata**


Change the global *name*, *owner*, or *description* metadata associated with a BSim server. A
BSim server URL is required.


**--name|-n** - specifies a formal, more
descriptive, name for the repository that can be used for the BSim client
display.


**--owner|-o** - gives a descriptive name
for the owner of the repository and/or the data it will contain.


**--description|-d** - specifies a short
string describing the intended contents of the new repository.


**getmetadata**


Show the global *name*, *owner*, and *description* metadata associated with a BSim server. A
BSim server URL is required.


**addexecategory**


Specify a new executable category to be included with generated metadata. A BSim
server URL and the name of the new category are required. This only affects future
ingest commands. Executables that have already been ingested are unaffected,
although they can be adjusted with an **generateupdates** command.


**date** - indicates the new category
holds date/time information.


**addfunctiontag**


Specify a new function tag to be included with generated metadata. A BSim server
URL and the name of the new tag are required. This only affects future ingest
commands. Functions that have already been ingested are unaffected, although they
can be adjusted with an **generateupdates**
command.


**dropindex**


Delete the main signature index from a BSim repository (in preparation for new
ingest). A BSim repository URL is required. Normal queries will not complete or
will be extremely slow.


**NOTE:** Not supported by H2 file database


**rebuildindex**


Recreate the main signature index (that had previously been dropped) for a BSim
repository. A BSim server URL is required. After this command completes, normal
function queries should be fast.


**NOTE:** Not supported by H2 file database


**prewarm**


Instruct a restarted BSim server to preload pages from the main signature index
and function table into RAM. This avoids slow random access disk reads on initial
queries. A BSim server URL is required.


**NOTE:** Not supported by Elasticsearch or H2 file databases


**generatesigs**


Generates function signatures and metadata for all program files retrieved from
a Ghidra Server repository or project as specified by a Ghidra URL. The generated
signatures may be retained as XML "sigs_" files within a specified XML storage
directory and/or committed to a specified BSim database specified with the **--bsim** option. If an XML storage directory is not
specified, a BSim URL must be specified to which the data will be committed.


The **--config|-c***&lt;config-template&gt;* option may be specified when generating
XML "sigs_" signature files in the absence of a BSim database (see
**createdatabase** for supported configurations). The generated files
will be written to the specified XML storage directory. Creation of the signature
files can also be achieved by specifying the **--bsim**
option instead of the **--config** option.


The **--overwrite** option may be specified when an XML storage directory has also been
specified to allow conflicting signature files to be overwritten.


The **--commit** option may be specified when a BSim URL has also been specified to allow
generated signatures to be committed to the BSim database. This option is implied
when a BSim URL has been specified without an XML storage directory.


**commitsigs**


Commit previously generated signatures and metadata (see
**generatesigs**) to a BSim repository. A URL specifying the BSim
repository and a path to a directory containing the "sigs_" XML files to commit are
required.


**--override***`<ghidraURL>`* - causes any Ghidra repository/project URL,
describing the storage repository and path of executables that was recorded in the
"sigs_" XML files during signature generation, to be overridden during the commit
operation with the specified Ghidra URL.


**generateupdates**


Generates updated function metadata for program files from a Ghidra Server
repository or project, as specified by a Ghidra URL, which previously had signature
and metadata generated (see **generatesigs**). Only metadata: names,
function tags, categories, etc. are changed. Signatures are not affected. The
generated updates may be retained as XML "update_" files within a specified XML
storage directory and/or committed to a specified BSim database specified with the
**--bsim** option. If an XML storage directory is not
specified, a BSim URL must be specified to which the data will be committed.


The **--config|-c***&lt;config-template&gt;* option may be specified when generating
XML "update_" files in the absence of a BSim database (see
**createdatabase** for supported configurations). The generated files
will be written to the specified XML storage directory. Creation of the update
files can also be achieved by specifying the **--bsim**
option instead of the **--config** option.


The **--overwrite** option may be specified when an XML storage directory has also been
specified to allow conflicting update files to be overwritten.


The **--commit** option may be specified when a BSim URL has also been specified to allow
generated updates to be committed to the BSim database. This option is implied when
a BSim URL has been specified without an XML storage directory.


**commitupdates**


Update a BSim repository with previously generated update metadata (see
**generateupdates**). A URL specifying the BSim repository and a path
to a directory containing the "update_" XML files to commit are required.


**listexes**


List all executable program records within a specified BSim database repository
which satisfy the specified criteria. A BSim URL specifying the repository must be
provided, and one of two options, **--md5** or **--name**, that indicate the specific executable must
also be given. All matching executable records will be listed.


**--md5|-m** - specifies an executable via its MD5
checksum as 32 hexidecimal digits.


**--name|-n** - specifies an executable
name which may match one or more executable records.


**--arch|-a** - specifies an architecture
as a Ghidra processor id which will be used to filter executables.


**--compiler** - specifies a compiler
specification id which will be used to filter executables.


**--sortcol|-s** - Specifies which display
column should be used to sort the results (**md5 | name**; default:
**md5**).


**--limit|-l** - specifies the maximum number of executables
to be listed which match the search criteria (default=20, a value of 0 indicates no
limit).


**--includelibs** - If specified, executable
records which correspond to a referenced Library will be included. Such records
have a fabricated MD5 which is based on its name.


**getexecount**


Get the total number of executable program records within a specified BSim
database repository which satisfy the specified criteria. A BSim URL specifying the
repository must be provided, and one of two options, **--md5** or **--name**, that indicate the specific executable must
also be given. All matching executable records will be listed.


**--md5|-m** - specifies an executable via its MD5
checksum as 32 hexidecimal digits.


**--name|-n** - specifies an executable
name which may match one or more executable records.


**--arch|-a** - specifies an architecture
as a Ghidra processor id which will be used to filter executables.


**--compiler** - specifies a compiler
specification id which will be used to filter executables.


**--includelibs** - If specified, executable
records which correspond to a referenced Library will be included. Such records
have a fabricated MD5 which is based on its name.


**delete**


Remove all records associated with a specific executable from a BSim repository.
A BSim URL specifying the repository must be provided, and one of two options,
**--md5** or **--name**, that indicate the specific executable must
also be given. All associated executable and function records are removed.
If an executable cannot be uniquely identified an error will result.


**--md5|-m** - specifies an executable via its MD5
checksum as 32 hexidecimal digits.


**--name|-n** - specifies an executable
name which may match one or more executable records.


**--arch|-a** - specifies an architecture
as a Ghidra processor id, when the **--name** option is not enough to uniquely specify the
executable.


**--compiler** - specifies a compiler
id string, when the **--name** option is
not enough to uniquely specify the executable.


**listfuncs**


List all function records associated with a specific executable from a BSim
repository. A BSim URL specifying the repository must be provided, and one of two
options, **--md5** or **--name**, that indicate the specific executable must
also be given. All associated executable and function records are listed. If an
executable cannot be uniquely identified an error will result.


**--md5|-m** - specifies an executable via its MD5
checksum as 32 hexidecimal digits.


**--name|-n** - specifies an executable
name which may match one or more executable records.


**--arch|-a** - specifies an architecture
as a Ghidra processor id, when the **--name** option is not enough to uniquely specify the
executable.


**--compiler** - specifies a compiler
id string, when the **--name** option is
not enough to uniquely specify the executable.


**--printselfsig** - If specified, each
function listed will be prefixed by a calculated self-significance score. This score is
expressed as a floating-point value.


**--callgraph** - If specified, a list
of all library functions called by the identified executable will be listed after
the function list.


**--printjustexe** - If specified, only a
summary of the executable will be displayed. If **--callgraph** was
also specified only the called libraries will be listed and not the specified
functions.


**--maxfunc** - specifies the maximum number of functions to
be listed which correspond to the identified executable (default=1000, a value of 0
indicates no limit).


**dumpsigs**


Dump signature and metadata from a BSim repository for a specific executable to
a "sigs_" XML file. A BSim server URL and a path to a directory where the new file
will be stored must be given. One of two options, **--md5** or **--name**, that specify the particular executable
must also be given.  If an executable cannot be uniquely identified an error will result.


**--md5|-m** - specifies an executable via its MD5
checksum as 32 hexidecimal digits.


**--name|-n** - specifies an executable
name which may match one or more executable records.


**--arch|-a** - specifies an architecture
as a Ghidra processor id, when the **--name** option is not enough to uniquely specify the
executable.


**--compiler** - specifies a compiler
specification id, when the **--name** option is not enough to uniquely specify the
executable.


**--Global
Options--**


These options apply to all **bsim**
commands.


**--user|-u***`<username>`* - specifies a user to masquerade as when connecting
to the server.


**--cert***&lt;certfile-path&gt;* - provides a path to the user's certificate when
connecting to a server that requires PKI authentication.


## Ghidra and BSim URLs


Ghidra utilizes Universal Resource Locators (URLs) to identify both *Ghidra
Server/Project Repositories* and *BSim Databases*. See the corresponding sections
below for specific formatting details. It is important to note that local *ghidra* and
*file* URLs never include a double-slash after the protocol (i.e, "://").


### Ghidra Server/Project Repository URLs


BSim command-line tools, as well as the Ghidra GUI, utilize a URL to specify the
location of a remote Ghidra Server repository or a local Ghidra Project. Both cases work in
a very similar fashion other than the format of the URL and potential limitations of a
local Project URL. Use of a Ghidra Server repository and corresponding URLs is preferred
since any Ghidra URL metadata added to a shared BSim database has the ability to be
accessed by other users, while a local Ghidra Project URL is very limited in its visibility
and path validity on other systems. For this reason, use of a local Ghidra Project URL
should be restricted to use with a local H2 BSim Database file.


The format of a remote *Ghidra Server URL* is distinctly different from a
*Local Ghidra Project URL*. These URLs have the following formats:


**Remote Ghidra Server Repository**


> ghidra://<hostname>[:<port>]/<repository_name>[/<folder_path>]


If the default Ghidra Server base port (13100) is in use it need not be specified with URL.
The *hostname* may specify either a Fully Qualified Domain Name (FQDN, e.g.,
*host.abc.com*) or IP v4 Address (e.g., *1.2.3.4*).


**Local Ghidra Project**


> ghidra:[/<directory_path>]/<project_name>[?/<folder_path>]


For local project URLs, the absolute directory path containing the project
**.gpr* locator file must be specified with the project name. The project name
should exclude any *.gpr/.rep* suffix. Only the '/' character should be used as a
directory separator. In addition, when running on Windows, the directory path should
include its drive designation preceded by a '/' (e.g., `ghidra:/C:/mydir/myproject?/folderA/folderB`).


### BSim Database URLs


BSim command-line tools utilize a URL to specify the type and specific details required
to establish a connection to a specific BSim Database. Within the Ghidra GUI the database
details are not specified using a URL and is done using an interactive form. Each BSim
database type has a distinct URL format:


> PostgreSQL postgresql://[<username>@]<hostname>[:<port>]/<dbname> Elasticsearch https://[<username>@]<hostname>[:<port>]/<dbname> Elasticsearch elastic://[<username>@]<hostname>[:<port>]/<dbname> H2 File file:[/<directory_path>]/<dbname>


The use of the *https* and *elastic* is equivalent.


> **Tip:** The inclusion of a <username> within a BSim URL
supercedes the concurrent use of the --user option which can still be used to control login to the Ghidra Server.  When a <username> has been specified within a BSim URL
a <password> may be included if neccessary,
albeit highly discouraged (e.g., postgresql://username:password@hostname/dbname ).
The password is appended to the username with a colon (':') separator and has limitations
on the characters which may be used.


![Warning: ](../icons/warning.help.png)Inclusion of a user
`<password>` within a BSim URL is highly
discouraged and only intended for use within restricted environments since the URL entry will persist
within the system process table and possibly within system log files.  This may be useful
in controlled situations where console password prompts cannot be handled.  Handling
the password prompt is preferred.


For local *file* URLs, the absolute path the H2 database **.mv.db* file
must be specified without the **.mv.db* extension. Only the '/' character should be
used as a directory separator. In addition, when running on Windows, the directory path
should include its drive designation preceded by a '/' (e.g., `file:/C:/mydir/mydb`).


---

[← Previous: BSim Control (bsim_ctl)](CommandLineReference.md) | [Next: Byte Viewer →](../ByteViewerPlugin/The_Byte_Viewer.md)
