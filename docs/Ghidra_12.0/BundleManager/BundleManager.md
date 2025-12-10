[Home](../index.md) > [BundleManager](index.md) > Ghidra Bundles

# Ghidra Bundles


## Dynamic modules


Scripting brings a powerful form of dynamic extensibilty to Ghidra,
where Java source code is (re)compiled, loaded, and run without exiting
Ghidra.  When a script grows large or requires external dependencies, it
might be worth the effort to split up code into *modules*.


To support modularity while preserving the dynamic nature of scripts,
Ghidra uses [OSGi](https://www.osgi.org).  Without delving too
much into terminology, the key things to know are


1. The unit of modularity in OSGi is the *bundle*.  Bundles are
*mostly independent* components with declared imports and exports.
2. Concretely, a bundle is a Jar file with extra metadata in its
manifest file that tells the framework what it uses/imports and what it
provides/exports.
Bundles are Jars, but Ghidra will automatically compile source
directories to bundles.  We refer to source directories intended to be
used in OSGi as [*source
bundles*](BundleManager.md#source-bundles). Each Ghidra script directory is a seperate
source bundle.
3. Bundles can *export* Java packages for use by other bundles,
and packages can have version numbers assigned.
4. Bundles can *import* packages from other bundles, and each
import can be constrained by version number or range.
5. The entire Ghidra API is part of the "system bundle", meaning its packages don't need
need to be explicitly imported.
6. A bundle can provide an *activator* class whose start and stop methods
are called when the bundle is activated/deactivated.


## Source bundles


When a directory is added to the Bundle Manager, it is treated as a
*source bundle*. When enabled, its Java contents are compiled to


```

        <user settings>/osgi/compiled-bundles/<hash>/

```


where `<hash>` is a hash of the source bundle path.  These compiled artifacts are then loaded
by the OSGi framework.


**NOTE:** The `<user settings>` directory is platform/configuration
specific. Its value can be found in the Ghidra Front End GUI, under `Help ->
Runtime Information -> Application Layout -> Settings Directory`


### Exploded Bundles


Each such subdirectory of `compiled-bundles/` is an *exploded
jar* --  by compressing it, we get a standard OSGi Jar bundle:


```

            jar cMf mybundle.jar -C <user settings>/osgi/compiled-bundles/<hash>  .

```


### Generated Files


If there is no manifest in the source directory, Ghidra generates one
using [bndlib](https://bnd.bndtools.org/) so that:


- Every package is exported unless it contains `private` or `internal` in its name.
- Packages listed in `@importpackage` meta-data are imported from active bundles.


Note: *import* and *export* here refer to inter-bundle dependency, see [below](#inter-bundle-run-time-dependency)


If no bundle activator is present, a stub is created and referenced in the generated manifest.


## Dependency


Two types of code dependency are available when developing with OSGi, intra-bundle and
inter-bundle.


### Intra-bundle (*compile time*) Dependency


Classes within a bundle, e.g. source files in a source bundle, can rely one another with
Java's usual package `import`.



This kind of dependency is resolved at
compile time -- if a class isn't imported or present, compilation will fail.


In the following example, `IntraBundleExampleScript` depends on `mylib.MyLibrary` without
any special dependency declaration since they are both defined in the same source bundle,
`my_ghidra_scripts`:


```

    my_ghidra_scripts/mylib/MyLibrary.java:
        package mylib;

        public class MyLibrary {
        	public void doStuff() {
        		// ...
        	}
        }

    my_ghidra_scripts/IntraBundleExampleScript.java
        // Intra-bundle dependency example.
        //@category Examples

        import ghidra.app.script.GhidraScript;
        import mylib.MyLibrary;

        public class IntraBundleExampleScript extends GhidraScript {
        	@Override
        	public void run() throws Exception {
        		new MyLibrary().doStuff();
        	}
        }

```


### Inter-bundle (*run time*) Dependency


To make use of code from *other* bundles, a bundle must declare its
dependencies.  When a bundle is activated, the framework attempts to
*resolve* its declared dependencies against active bundles.  The
first match, in the order of bundle activation, will be "wired" to
the dependent.


Note: OSGi bundle dependency is very similar to Java 9 modules. The key difference is that
Java 9 modules provide *load time* resolution, while OSGi provides *run time*
resolution.


#### `@importpackage` in a script


Ghidra's `@importpacakge` meta-data tag provides a convenient way to declare inter-bundle
dependencies directly in a script. Set the value to a comma separated list of packages
to import from other bundles.


In the example below, the class `InterBundleExampleScript` is implemented in the bundle
`my_ghidra_scripts` and uses a class, `yourlib.YourLibrary`, defined in another bundle,
`your_ghidra_scripts`.


```

    your_ghidra_scripts/yourlib/YourLibrary.java:
        package yourlib;

        public class YourLibrary {
        	public void doOtherStuff() {
        		// ...
        	}
        }


    my_ghidra_scripts/InterBundleExampleScript.java
        // Inter-bundle dependency example.
        //@category Examples
        //@importpackage yourlib

        import ghidra.app.script.GhidraScript;
        import yourlib.YourLibrary;

        public class InterBundleExampleScript extends GhidraScript {
        	@Override
        	public void run() throws Exception {
        		new YourLibrary().doOtherStuff();
        	}
        }

```


#### `Import-Package` in the manifest


The underlying OSGi mechanism for declaring inter-bundle dependency is via the manifest.


You can find detailed descriptions of manifest attributes used by OSGi, like `Import-Package`, here
[https://osgi.org/specification/osgi.core/7.0.0/framework.module.html#framework.module.importpackage](https://osgi.org/specification/osgi.core/7.0.0/framework.module.html#framework.module.importpackage).



If a Ghidra source bundle has no manifest, Ghidra [generates one](#generated-files).


For example, the `@importpackage yourlib` in the previous example corresponds to the `yourlib` entry
in the `Import-Package` line of the manifest generated for `my_ghidra_scripts`:


```

     <user settings>/osgi/compiled-bundles/ab12cd89/META-INF/MANIFEST.MF:
        Manifest-Version: 1.0
        Bundle-ManifestVersion: 2
        Export-Package: mylib
        Import-Package: ghidra.app.script,yourlib,ghidra.app.plugin.core.osgi
        Require-Capability: osgi.ee;filter:="(&(osgi.ee=JavaSE)(version=21))"
        Bundle-SymbolicName: ab12cd89
        Bundle-Version: 1.0
        Bundle-Name: ab12cd89
        Bundle-Activator: GeneratedActivator

```


The manifest generated for `your_ghidra_scripts` is as follows:


```

     <user settings>/osgi/compiled-bundles/ef34ab56/META-INF/MANIFEST.MF:
        Manifest-Version: 1.0
        Bundle-ManifestVersion: 2
        Export-Package: yourlib
        Import-Package: ghidra.app.plugin.core.osgi
        Require-Capability: osgi.ee;filter:="(&(osgi.ee=JavaSE)(version=21))"
        Bundle-SymbolicName: ef34ab56
        Bundle-Version: 1.0
        Bundle-Name: ef34ab56
        Bundle-Activator: GeneratedActivator

```


Notice the `Export-Package` line generated for `your_ghidra_scripts`.  The generated
manifest exports all packages not including `private` or `internal`.


For full control, users can include a manifest with their bundle's source,
e.g. `my_ghidra_scripts/META-INF/MANIFEST.MF`.


## Enabling and disabling bundles


For a bundle's contents to be available (e.g. for loading classes), its [OSGi state](https://docs.osgi.org/specification/osgi.core/7.0.0/framework.lifecycle.html#d0e9143) must be "`ACTIVE`".  Ghidra generally takes care of this, but
the following provides more details about the underlying OSGi for debugging.


Ghidra activates a bundle when added, enabled, or when a script contained within is
run.

When enabled, the root directory of a source bundle is also scanned for Ghidra scripts
and any found are added to the script manager.


When *dis*abled, any dependents of a bundle are stopped/deactivated first, then
the bundle itself is stopped. Its scripts are then removed from the script manager.


The color of each bundle path reflects state as follows:


- error - e.g. the bundle file is missing
disabled - Ghidra knows the
path, but that's it
inactive - scripts are visible in the script
manager, but no classes are loaded.  A bundle moves into this state when its
dependencies become inactive (e.g. by being disabled), one of its scripts is deleted, or its cache is [cleaned](#cleaning-bundles)
active - the bundle is built and classes within
can be loaded


The normally hidden column "OSGi State" is also available.  In addition to the Bundle
state, this column will report


- (DISABLED) - if the bundle is disabled
(ENABLED) - if the bundle is enabled, but the bundle manager has no handle to it.
If this state persists, there is likely an internal error
(UNINSTALLED) - if the bundle is enabled, but the framework has released its handle.
This is typical for an inactive bundle


## Adding and removing bundles from the manager


Adding a directory to the bundle manager will also enable it, so scripts within become
available in the script manager.


Removing a bundle disables it, so its scripts will be removed from the script manager
and its dependents will become inactive.


## Cleaning bundles


When Ghidra builds a source bundle, the results are written to the
directory

`<user settings>/osgi/compiled-bundles/<hash>`.

These files can then be loaded by the OSGi framework.


A *clean* deactivates then wipes this subdirectory for each selected bundle and
clears its build summary.


If a source bundle's imports aren't available during build, some source files can
produce errors.  In order to force Ghidra to recompile, one must either modify the files
with errors or *clean* the bundle then re-enable.


## Refresh bundles


Refresh will deactivate, clean, then reactivate every enabled bundle.


**Related Topics:**


- [Scripting](../GhidraScriptMgrPlugin/GhidraScriptMgrPlugin.md)


---

[← Previous: Ghidra Script Development](../GhidraScriptMgrPlugin/ScriptDevelopment.md) | [Next: Jython Interpreter →](../Jython/interpreter.md)
