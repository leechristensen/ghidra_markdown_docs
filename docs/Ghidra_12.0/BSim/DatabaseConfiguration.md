[Home](../index.md) > [BSim](index.md) > Tailoring BSim Meta-data

# Database Configuration


## Overview


The server for the BSim Database is distinct from the traditional Ghidra server,
although for many use cases it is convenient to have both running and view the BSim server
as a loosely coupled extension to the base Ghidra Server. In terms of start-up, shutdown,
and configuration however, the two servers are completely separate.


There are two choices for deploying a shared server for the BSim Database: PostgreSQL or
Elasticsearch. Both options support multiple users and allow multiple simultaneous connections
to the remote server.  A single database can ingest large datasets, while
still maintaining short query times.


Alternately, a single user can create a BSim database on their local file-system,
without a server, by utilizing the H2 database engine integrated into Ghidra. This option
is intended for querying against small datasets and does not require installation of
additional server software.


A PostgreSQL server, which must be built with a BSim specific extension,
runs on a single host and makes efficient use of whatever CPU, memory, and disk resources
are made available to it. PostgreSQL is a robust and capable server that should perform well
on minimally configured workstations up to high-end production hardware. Source for the
BSim extension to PostgreSQL is included as part of the Ghidra installation, but the
PostgreSQL source may need to be obtained separately by the database administrator.
See [“Building the Server”](DatabaseConfiguration.md#building-the-server)


An Elasticsearch server, which must have a BSim specific plug-in installed, runs
as a scalable database that automatically distributes itself across machines in a cluster,
allowing individual database queries and requests to be serviced in parallel. The Elasticsearch
BSim plug-in is included with the Ghidra installation, but the core server software must be obtained
separately by the database administrator.
See [“Installing the Plug-in”](DatabaseConfiguration.md#installing-the-plug-in)


BSim clients included in the base Ghidra distribution can interface to any of these
databases. Users that just want to connect to an existing shared server via a BSim client do not need to
install any server software themselves.


## Server Configuration


### PostgreSQL Configuration


#### Building the Server


In order to use PostgreSQL as a BSim server, it must be built with a BSim specific
extension, provided as part of the Ghidra installation. Prebuilt servers, like those
provided as OS distribution packages, will not work as is with BSim. For users on Linux
and macOS, the Ghidra installation provides a script, `make-postgres.sh`,
in the module directory `Ghidra/Features/BSim/support` that builds both the PostgreSQL
server and the BSim extension from source and prepares the installation for use with
Ghidra.  If not already included in the Ghidra installation, the source distribution
file, currently `postgresql-15.13.tar.gz`, can be obtained from the PostgreSQL
website at


> https://www.postgresql.org/ftp/source/v15.13


The steps to build the PostgreSQL server with the BSim extension then are:


1) If not already present, place the PostgreSQL source distribution file
`postgresql-15.13.tar.gz` in the Ghidra installation at


> $(ROOT)/Ghidra/Features/BSim/support/postgresql-15.13.tar.gz


2) From the command-line, within the same directory, run the script `make-postgres.sh`


> cd $(ROOT)/Ghidra/Features/BSim/support ./make-postgres.sh


Additional packages or software may need to be installed on the host OS in order for the
build to complete successfully, OpenSSL in particular is required for BSim.  For the
full list of PostgreSQL software dependencies, refer to:


> https://www.postgresql.org/docs/15/install-requirements.html


Once the build has completed successfully,
the **bsim_ctl** command-line script is ready to use
for starting a server (see
[“Starting and Stopping the Server”](DatabaseConfiguration.md#starting-and-stopping-the-server)).
The PostgreSQL server software will run out of the Ghidra installation at


> $(ROOT)/Ghidra/Features/BSim/build/os/linux_x86_64/postgresql
OR $(ROOT)/Ghidra/Features/BSim/build/os/linux_arm_64/postgresql
OR $(ROOT)/Ghidra/Features/BSim/build/os/mac_x86_64/postgresql
OR $(ROOT)/Ghidra/Features/BSim/build/os/mac_arm_64/postgresql


Other than having the extension itself, a BSim enabled PostgreSQL server is completely standard,
and can be configured like any other stand-alone PostgreSQL server. There are no direct restrictions
on modifying the configuration values. A default configuration is provided with this installation that
has been tuned specifically for the BSim Database application, so in practice there may be little reason to
modify it. But there are a few standard configuration values for the server that might need
adjusting. See
[“Additional Configuration”](DatabaseConfiguration.md#additional-configuration).


#### Starting and Stopping the Server


The basic start-up and shut-down is accomplished with the same command-line script,
which takes either the keyword **start** or
**stop** as the first parameter. The second
parameter must be an absolute path to the chosen data directory.


> $(ROOT)/support/bsim_ctl start
/path/to/datadir $(ROOT)/support/bsim_ctl start /path/to/datadir
--port 8000 $(ROOT)/support/bsim_ctl stop
/path/to/datadir $(ROOT)/support/bsim_ctl stop /path/to/datadir
force


The data directory should already exist and should initially not contain any files.
The first time a server is started for a particular data directory, a large number of
configuration files and other sub-directories associated with the PostgreSQL server
will automatically be created. Upon subsequent restarts the existing configuration will
be reused.


The **start** command can take an optional
**--port** parameter. This can be used to specify
a non-standard port for the PostgreSQL server to listen on. In this case, any
subsequent reference to the BSim server, in the Ghidra client, or with the **bsim** command described below, must specify the port.
When using the **bsim** command, a
non-default port must be explicitly specified with the BSim **postgresql://** URL (see [“Ghidra and BSim URLs”](CommandLineReference.md#ghidra-and-bsim-urls) for more
details).


The **stop** command can take the keyword
**force** as an optional parameter. Without
this, the shutdown of the server will wait until all currently connected clients finish
their sessions. Adding this parameter will cause all clients to be disconnected
immediately, rolling back any transactions, and the server will shutdown
immediately.


#### Security and Authentication


BSim makes use of PostgreSQL security mechanisms to enforce privileges and
authenticate users. The **bsim_ctl** command
wraps the subset of functionality described here, but other adjustments are possible by
connecting directly to the server and issuing SQL commands.


The PostgreSQL server, as configured for BSim, only accepts connections via SSL, so
communications in transit are always encrypted regardless of the authentication
settings.


PostgreSQL uses the concept of *roles* to grant
access privileges based on particular users. Generally, a user's role is determined by
the *username* used to establish the connection.
For BSim, each user role is granted one of two privilege levels: **user**, which allows read-only access to the server for
normal queries, and **admin**, which
additionally allows database creation, ingest, update, and deletion.


BSim supports three different authentication methods, when connecting as a client or
during database ingest and maintenance. This method is established for a server by the
initial **start** command.


**trust**


`bsim_ctl start /path/to/datadir
--auth trust`


This is currently the default. No authentication is performed and privilege
is granted based on the user name presented. Masquerading is possible.


**password**


`bsim_ctl start /path/to/datadir
--auth password`


Users are authenticated via password. A default password 'changeme' is
established when the new user is created. Passwords can be changed by the user
from the BSim client or can be reset by an administrator via the **resetpassword** command.


**pki**


`bsim_ctl start /path/to/datadir --auth pki
--cafile "/path/to/rootcert"`


Users are authenticated by PKI certificates. Upon initialization, the BSim
server must be provided (via the **--cafile** option) a file containing the public keys
for the certificate authorities used to issue user's certificates. The file
consists of the authoritative certificates in PEM format concatenated
together.


BSim users must register their certificate with the Ghidra client using the
*Edit-&gt;Set PKI Certificate...* menu
option from the Project dialog. The BSim client will automatically submit the
certificate to a server that requests it, and the password to unlock it will be
requested as needed. This is the same mechanism used to a access a PKI
protected Ghidra server, and if a user needs access to both a BSim server and
Ghidra server that are PKI protected, the servers should probably be configured
with the same certificate authorities so that they will accept the same
certificate from the user.


With PKI authentication enabled, at the time a new user role is established
with the server, the X.509 Distinguished Name, as bound to the user's
certificate, must be associated with the user name via the **--dn** option. See [“Adding Users to the
Database”](#adding-users-to-the-database).


The authentication method should be established once, the first time the **start** command is issued for the server on an
empty data directory. Subsequent restarts of the server will not change these settings.
If the settings really need to be changed, the **changeauth** command can be issued. It takes the same
options as the **start** command and can only
be run if the server is shutdown first.


> $(ROOT)/support/bsim_ctl changeauth
/datadir/path --auth password


Using the **changeauth** command on a
server with an established set of users will likely require other disruptive changes to
create passwords or associate Distinguished Names with users, if they didn't exist
before.


If it is determined that only the database administrators have OS level, local,
access to the server's host machine, they can choose to use the **noLocalAuth** option as part of the **start** or **changeauth** commands. This disables authentication for
users connecting to the server by the 'localhost' interface. This may facilitate the
use of scripts for ingest etc., where working with passwords is cumbersome.
Authentication is still enforced for any remote connection.


#### Adding Users to the Database


The username used to start the server for the first time, causing the initialization
of the data directory, becomes the administrator for that server. No other
username/role is initially known to the server. New usernames/roles can be added to the
server using the following command:


> $(ROOT)/support/bsim_ctl adduser /path/to/datadir username $(ROOT)/support/bsim_ctl adduser /path/to/datadir username --dn "C=US,ST=MD,CN=Firstname User"


If password authentication has been set for the server, the new user's password will
initially be set to 'changeme'. If PKI authentication has been set for the server, The
Distinguished Name, as bound to the new user's certificated must be provided when
issuing the **adduser** command, via the
**--dn** option. The Distinguished Name must
be presented as a string containing a comma separated sequence of attribute/value pairs
that uniquely identifies a certificate. Currently, the Common Name (CN=) is the only
attribute inspected by the PostgreSQL server, so other attributes can be omitted.


New users are by default only given **user** permissions, meaning that they can only place
queries to the database and cannot ingest, update, or delete data. The new user can be
given **admin** privileges (by an existing
administrator) by issuing the command:


> $(ROOT)/support/bsim_ctl changeprivilege username admin


#### Additional Configuration


The relevant configuration files are at the top level of the data directory:


> postgresql.conf pg_hba.conf


The most important configuration parameters in `postgresql.conf` are:


**shared_buffers**


This controls the amount of RAM available for caching database pages across
all connections to the server. The default should be reasonable in most
situations, but for large databases or many simultaneous connections it might
make sense to increase this.


**max_wal_size**, **checkpoint_timeout**


These control how often the server forces database pages to be written back
out to the file-system. The defaults are set to minimize disk writes when
ingesting large numbers of records in one session. There should be little
reason to change these values.


**ssl_min_protocol_version**


This controls the minimum SSL/TLS protocol version used when the server negotiates a connection.
The current default is 'TLSv1.2'


The `pg_hba.conf` file is used to configure which
connections the server accepts for a particular outward facing IP address and what
security mechanisms are enforced for those connections. Currently all addresses are
configured to accept SSL connections only, except possibly for 'localhost'.
Administrators *can* currently filter connections
based on usernames and the particular database (which corresponds to Ghidra's concept
of *repository*).


> **Warning:** Warning By default, the server accepts all connections from all users.


#### Configuration Defaults


There is a `serverconfig.xml` which contains a few of
the default configuration values that are most crucial for the BSim Database. **Beware:** This file is currently parsed only once
for the entire *lifetime* of a particular data
directory: it is read only when the data directory is first initialized, i.e. the first
time the **bsim_ctl start** command is
invoked on the empty directory. This file is intended to provide reasonable defaults
that are different from the standard PostgreSQL defaults. To provide site specific
configuration, changes should be made to the normal PostgreSQL configuration files.


#### PostgreSQL Firewall Considerations


Remote client access to the PostgreSQL server may have network firewalls
which must be considered and properly configured to allow network access.
Both dedicated network firewalls and OS-level firewalls must be considered.


Firewall configurations are beyond the scope of this document, however for simple
single-node installations on Linux the `firewall-cmd`
may be used to allow incoming connections to the appropriate port (TCP port 5432 is the
default for PostgreSQL).  This does not consider network firewall devices which may
also impact connectivity.


```

    sudo firewall-cmd --permanent --add-port=5432/tcp && sudo firewall-cmd --reload

```


NOTE: The above Linux firewall command assumes the `firewalld`
package has been installed on the system.


### Elasticsearch Configuration


A full description of how to configure an Elasticsearch cluster is beyond the scope of
this document. In particular, the **bsim_ctl**
command-line, as described in [“PostgreSQL Configuration”](DatabaseConfiguration.md#postgresql-configuration), does not apply to
Elasticsearch. Complete documentation for administering a database is available on-line
from the Elasticsearch website.


The following discussion describes how to set up a toy, or single node, server, using the
free and open Elasticsearch distribution. This distribution includes a REST API for administering
a database, which can be accessed using `curl` commands or some other method
to send HTTP requests directly to the node.


#### Installing the Plug-in


In order to make use of Elasticsearch with BSim, the database administrator must
install the *lsh.zip* plug-in as part of the
Elasticsearch deployment. The plug-in is available in the Ghidra extension named *BSimElasticPlugin*
(`<ghidra-install-dir>/Extensions/Ghidra/ghidra_11.2.1_U_20241105_BSimElasticPlugin.zip`).
The extension may be unzipped to a temporary location or use Ghidra's Install Extensions
capability which will unpack it into the users platform-specific config directory
indicated in the detail view of the Install Extensions window.  The extension is not
used directly by Ghidra and is only needed for the
*lsh.zip* elasticsearch plug-in
which must be installed on every node of the cluster
before a BSim repository can be created. The description below shows how to enable
the BSim plug-in for a single node, but this will need to be repeated for any
additional nodes.


> **Tip:** Refer to the README.md file within the unpacked extension for important plugin details.  The plugin file
stipulates a specific elasticsearch version and may require an adjustment and repack.


Assuming the add-on has been unpacked, the plug-in can be installed to a single node
using the *elasticsearch-plugin* command in the
*bin* directory of the node's Elasticsearch
installation.


> bin/elasticsearch-plugin install
file:///path/to/ghidra/extension/BSimElasticPlugin/data/lsh.zip


Replace the initial portion of the absolute path in the URL to point to the Ghidra
installation. Once the plug-in is installed, the toy deployment can be (re)started from
the command-line by running


> bin/elasticsearch


This will dump logging messages to the console, and you should see `[lsh]` listed among the loaded plug-ins as the node starts
up.


#### Elasticsearch Security


The open Elasticsearch distribution starts with password authentication
enabled by default.  When a node is started up for the first time, as described above, an
**elastic** user is created with a randomly
generated password that is reported, once, to the console. For a toy deployment, it may
be convenient to add additional users via `curl` commands. The
following example creates a user named **ghidrauser**
with a default password "changeme", using the **elastic** users credentials.
The generated password for the **elastic** user must be substituted for the XXXXXX
at the beginning of the command.


```

curl -k -u elastic:XXXXXX -X POST "https://localhost:9200/_security/user/ghidrauser?pretty" -H 'Content-Type: application/json' -d'
{
  "password" : "changeme",
  "roles" : [ "viewer" ],
  "full_name" : "Ghidra User",
  "email" : "ghidrauser@example.com"
}
'

```


Elasticsearch uses the concept of *roles* to grant access privileges to particular users. The
built-in role **viewer**, as in the example above, can be used to grant users
read-only access to a database.  The built-in **superuser** role grants
administrator privileges.


#### The Elasticsearch URL


Assuming an Elasticsearch cluster is running and the plug-in has been properly
installed, all other parts of BSim interact transparently with the cluster. The **bsim** command, described in [*Ingesting
Executables*](IngestProcess.md), and the Ghidra/BSim client, described in [*Querying a BSim
Database*](../BSimSearchPlugin/BSimSearch.md), require no additional configuration to work with Elasticsearch,
except users must provide the correct URL to establish a connection. Elasticsearch
communicates over *https*, and BSim clients
automatically assume they are communicating with Elasticsearch when they see this
protocol. Alternatively, the protocol may be specified as *elastic* when using the **bsim** command. Elasticsearch use by BSim assumes a
default port of 9200 unless otherwise specified when specifying the server host. See [“Ghidra and BSim
URLs”](CommandLineReference.md#ghidra-and-bsim-urls) for additional information about URLs.


#### Elasticsearch Firewall Considerations


Remote client access to the Elasticsearch server/cluster may have network firewalls
which must be considered and properly configured to allow network access.
Both dedicated network firewalls and OS-level firewalls must be considered.


Firewall configurations are beyond the scope of this document, however for simple
single-node installations on Linux the `firewall-cmd`
may be used to allow incoming connections to the appropriate port (TCP port 9200 is the
default for elasticsearch).  This does not consider network firewall devices which may
also impact connectivity.


```

    sudo firewall-cmd --permanent --add-port=9200/tcp && sudo firewall-cmd --reload

```


NOTE: The above Linux firewall command assumes the `firewalld`
package has been installed on the system.


## Creating a Database


If using either PostgreSQL or Elasticsearch the server must be properly configured and
running before a **database** can be created. In the
case of an H2 file-based database there is no server requirement. Only after a database has
been created can data be ingested or queries performed. In this context, a database is a
single container of reverse engineered functions. Metadata pertaining to executables and
call-graph relationships is also stored, but the principle database record describes a
*function*. A single PostgreSQL or Elasticsearch
server can hold multiple independent databases.


A database is created using the **bsim**
command script. The basic command looks like


> $(ROOT)/support/bsim createdatabase bsimURL config_template


A BSim database is completely distinct from the Ghidra Server or Ghidra project, so the
executables and functions contained within do not need to coincide at all.


The Ghidra GUI client specifies a BSim database with its explicit characteristics (i.e.,
DB type, name, host/port if applicable, etc.), while the **bsim** command accepts a *bsimURL* which includes similar details (see [“Ghidra and BSim URLs”](CommandLineReference.md#ghidra-and-bsim-urls) for more
details).


The *config_template* parameter passed to **bsim createdatabase** names a collection of specific
configuration values for the newly created database. A standard Ghidra distribution
provides a number of predefined templates (See below) designed for specific database use
cases. It is simplest to use a predefined template when creating a database, but it is
possible to edit an existing template or create a new template (See [“Creating Database Templates”](DatabaseConfiguration.md#creating-database-templates)).


There are two critical database properties being determined by the template that need to
be kept in mind: the **index tuning** and the **weighting scheme** relative to the size of the database.
The two pieces of the template name, separated by the '_' character, refer to these
concerns.


The index tuning affects the use of the database by trading off between, the time
required to perform individual queries, the amount of variation between matching functions
a query can tolerate, and the amount of storage required per database record. Ideally, the
database is tuned, before the initial ingest occurs, to the *anticipated size* of the database. The database can trade off
storage size (per record) and latency for overall query response time, but the decision
needs to be made before the database is populated. Currently there is a **medium** tuning that is ideal for repositories that will store
on the order of 10 million functions. There is also a **large** tuning, which uses more storage but can maintain fast
query times for databases with 100 million functions or more. There is a large overlap for
these tunings, so if its unclear how large a database might grow, go ahead and use the
medium tuning.


The weighting scheme affects how BSim views the relative importance of individual code
constructs within a function. Code constructions are extracted as *features*, and each feature is assigned a weight. The basic
schemes are: **32** for 32-bit compiled code, **64** for 64-bit code. The scheme that matches the
predominant form of code in the repository being ingested should be used. Mixed schemes are
possible, but a corpus which is predominantly 32-bit, even with a small number of 64-bit
executables mixed in, should still use the 32-bit weights.


There are some weighting schemes designed for more specialized code. The **64_32** scheme is for 64-bit code using 32-bit pointers. The
**nosize** scheme allows better matching of 32-bit
functions to 64-bit functions, when they are compiled from the same source. The **cpool** scheme is designed for Java byte-code or Dalvik
executables. For more discussion of weighting, see [“Weighting
Software Features”](FeatureWeight.md#weighting-software-features).


The full template name incorporates both an index tuning and a weight scheme. Some
common examples of template names:


**medium_32**


A medium index tuning with a weighting scheme designed for 32-bit
executables.


**medium_64**


A medium index tuning with a weighting scheme designed for 64-bit
executables.


**large_32**


A 32-bit weighting scheme with tuning for a large database size.


**medium_cpool**


A medium index tuning with a weighting scheme for Java executables.


**medium_nosize**


A medium index tuning with a weighting scheme allowing matches between 32-bit
and 64-bit code.


## Tailoring BSim Metadata


There is some facility to tailor a specific BSim database instance so that it can ingest
and/or report information about executables or functions to make results more useful for a
specific project or user. Capabilities can be added after a database has been created and
is running by issuing specific **bsim** commands,
but they can also be added to a *configuration
template* prior to creating the database, which provides a record of the
specific additions should the database instance need to be recreated or multiple tailored
instances be deployed. For additions that allow the ingest of more metadata about
executables or functions, users must provide additional scripts to Ghidra during the ingest
process in order to read in or discover the new metadata.


The **Name**, **Owner**, and **Description** associated with a BSim instance can be trivially
tailored with the **bsim setmetadata**
command.


> $(ROOT)/support/bsim setmetadata bsimURL --name "BSim Database" $(ROOT)/support/bsim setmetadata bsimURL --owner "Administrators" $(ROOT)/support/bsim setmetadata bsimURL --description "Files of interest"


This information is displayed in various windows by the BSim client. The values can be
changed at any time and do not otherwise affect the records contained in the database.
Multiple command-line parameters can be fed to **bsim
setmetadata** so long as each one starts with **--name**, **--owner**, or
**--description** respectively. Quoting of values may be
necessary to get some strings to be interpreted as a single command-line parameter.


### Executable Categories


BSim provides the powerful ability to associate new types of metadata with each
executable that the database ingests. Any method of categorizing executables that
describes an executable with a simple string value, referred to here as an executable
**category**, can be added as a field to the
database. With only minor adjustments to the ingest process, new category values can be
automatically attached to incoming executables and are treated like any other executable
field that BSim understands. Category values are retrieved with queries, can be used for
filtering, and show up as sortable columns in result tables.


All categories have a formal name (or type), which is used both in the ingest process
(See below) and as the label for table columns. The name can contain alphanumeric
characters or punctuation from the limited set, ' ._:/()'. For each executable there can
be zero, one, or more *string* values associated
with the category. No value is required for the executable, and any single value can be
used for filtering (either the executable is labeled with the value or it is not) even if
there are multiple values for that category. If there are multiple values, a query that
matches the executable will return all the values as a single sorted column entry.


It is also possible to create a special time-based category. This category can have
any name as above, but instead of associating string values with the executable, it
associates a single time-stamp. The time-stamp has precision down to the millisecond and
provides filtering and sorting based on time. Internally, this new category repurposes
the column storage originally providing an executable's *Ingest
Date* field. As a result, any BSim instance
can have only one time category and only one time-stamp within it. The ingest scripting
must provide any actual time-stamp value for the executable, or the database will fill in
the "epoch", 12:00 am, Jan 1, 1970.


A new category can be added to the database at any time using the **bsim addexecategory** command.


> $(ROOT)/support/bsim addexecategory bsimURL MyCategoryName $(ROOT)/support/bsim addexecategory bsimURL MyTimeField date


The single time-stamp field can be renamed by appending the keyword "date" to the
command after the name of the category. Once a category is added, the corresponding program
options set for any new executables will automatically read into the database as part of
the ingest process. Previously ingested executables, assuming they have the new program
options set, can be updated within the BSim database using one of the **bsim generateupdates** command variants. In either case, the
relevant program options typically need to be filled by running a Ghidra script (See [“Ingesting Executable Categories”](IngestProcess.md#ingesting-executable-categories)).
There is currently no method for deleting a category once it has been created.


### Function Tags


BSim can be configured to recognize specific **Function
Tags**, which are named Boolean properties on individual functions within
an executable. Within a Ghidra program, any number of different function tags can be
established by the user and are used to label individual functions or specific subsets of
functions that share a particular property. This would typically be used to label classes
of functions that are important to analysts, unpacked functions could be labeled with the
tag *UNPACKED* for instance.


In order for BSim to recognize specific function tags, they must be individually
registered with the BSim database. These tags are then automatically ingested into the
database, along with the other standard metadata describing functions, and can be used to
filter match results when querying the database. A function tag has a formal name, which
can be displayed as part of the function header within the main code browser and is used
for BSim columns and filter labels. Once the tag is created for a program, functions
universally have the tag as a Boolean property, either the name applies to a function or
it doesn't, and arbitrary subsets can be *tagged*
with that name.


A tag must be *registered* with a BSim database
before it can be used as a filter or seen in results. A tag can be registered at any time
with the **bsim addfunctiontag** command.


> $(ROOT)/support/bsim addfunctiontag bsimURL MyTagName


The new tag will automatically be read in when any new executables are ingested. If
previously ingested executables already had the new tags before they were registered,
their metadata within BSim database can be updated using the **bsim generateupdates** command variants. BSim is limited to 29
registered tag names, and there is currently no way to remove a tag once it has been
registered.


### Creating Database Templates


It is possible to create tailored database configuration templates so that
implementers have a permanent and accessible record of a particular set-up and don't need
to repeatedly issue **bsim setmetadata** and
**bsim addexecategory** when creating a
database. Other aspects of a database can also be manipulated, like weighting schemes and
index tuning, but doing this properly is beyond the scope of this document. A **database template** is the basic set of configuration
parameters used to set up BSim database instance. The configuration parameters are
established for a particular database when the **bsim
createdatabase** command is run (See [“Creating a
Database”](DatabaseConfiguration.md#creating-a-database)). The template name passed on the command-line actually identifies an
XML file-name, appended with the '.xml' suffix, in the directory:


> $(ROOT)/Ghidra/Features/BSim/data


The file has a root tag of *`<dbconfig>`*,
and the first child tag of this root is the *`<info>`* tag. This tag contains all the metadata tags that
can be easily changed or added to the database. A list of the metadata tags follows. The
metadata is provided as formal text content within the tag, and none of the tags
currently take attributes.


> XML Tag Description <name> Name of the database <owner> Owner of the database <description> An overarching description of the database <major> Major decompiler version used for ingest (Should be set to zero) <minor> Minor decompiler version used for ingest (Should be set to zero) <settings> Specific settings for the signature strategy (Should be set to zero) <execategory> The name of an executable category (to be) defined for this database
instance <datename> The name of the timestamp column <functiontag> The name of a function tag (to be) registered with this database
instance


There can be multiple *`<execategory>`* tags
if more than one category is desired and both *`<execategory>`* and *`<datename>`* are optional tags. The date column name
defaults to 'Ingest Date' and is drawn from the corresponding Ghidra program option. The
tag order needs to be preserved. There can be multiple *`<functiontag>`* tags, one for each function tag to be
registered with the database.


It is easiest to copy an existing template and just edit the tags described above. The
remaining tags in the file are more dangerous to manipulate. The *`<k>`* and *`<L>`*
tags pertain to the index tuning. The *`<weightsfile>`* tag gives the name of the weights file,
within the same directory, which is also another XML file. It is simplest to choose from
the existing weight files provided with the distribution. See [“Weighting Software Features”](FeatureWeight.md#weighting-software-features).


---

[← Previous: Creating a Database](DatabaseConfiguration.md) | [Next: Ingesting Executables →](IngestProcess.md)
