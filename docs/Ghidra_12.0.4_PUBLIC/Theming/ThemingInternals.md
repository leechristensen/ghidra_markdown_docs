[Home](../index.md) > [Theming](index.md) > Architecture

# Theming Architecture


This document describes the API for initializing and managing themes. A theme (the
`GTheme`
class) in Ghidra represents a specific Look and Feel as well the set of values for the color,
font, and icon resource IDs used in the application. Resource IDs are defined in theme properties
files.   Application writers refer to these IDs when using colors, fonts and icons.
The `Gui` class provides a set of
static methods that serves as the primary interface for managing all aspects of theming.


## GTheme Class


The `GTheme` class is the implementation of the theme concept. At any given time,
the application is using resource values as specified by the active theme. The theme specifies
the Java Look and Feel, whether or not the overall theme is "dark" (which determines which default
values to use) and any resource values which have been overridden specifically by that theme.
There are two types of themes; built-in themes and file-based themes. Built-in
themes are implemented directly as sub-classes of `GTheme` and simply specify a
Java Look and Feel
and whether or not the theme is "dark". There is one "built-in" theme for each supported
Look and Feel. File-based themes read their values from a theme file. Theme files are created by
editing and saving existing themes.


## GThemeValueMap / ThemeValue Classes


These are the base classes for storing values for resource IDs. A `GThemeValueMap`
consists of three maps, one each for colors, fonts, and icons. Each map binds an ID to a
appropriate subclass of `ThemeValue`, which is the base class for
`ColorValue`, `FontValue`, and
`IconValue`. Resource values are stored in these `ThemeValue` sub-classes
because the value can be
either a concrete value or a reference to some other resource of the same type. So, for
example, "color.bg.foo" could map directly to an actual color or its value could be a reference
to some other indirect color like "color.bg.bar". In any `ThemeValue` object, either
the referenced ID or the direct value must be null. To get the ultimate concrete value, there
is a convenience method called `get()` on `ThemeValue`s that takes a
`GThemeValueMap` as an argument.
This method will recursively resolve reference IDs, which is why it needs a value map as an
argument.


`GThemeValueMap`s have some convenience methods for performing set operations.
You can load
values from other `GThemeValueMap`s into this map, which adds to the current map,
replacing values with the same ID with values from the other map. Also, there is a method for
getting the differences from one GThemeValueMap to another.


## Gui Class


The `Gui` class is a set of static methods that provides the primary API for
managing themes.
It has methods for switching themes, adding themes, deleting themes, saving themes, restoring
themes, getting/setting values for resource IDs, adding theme listeners, and others.  This
class is meant to be used by application developers, along with `GColor` for colors
and `GIcon` for icons.   Fonts are handled slightly differently by making calls to
`Gui.registerFont(Component, Id)`


## Application Initialization


Applications need to call `Gui.initialize()` before any uses of color, fonts, or
icons occur.
This will load all resource defaults from all `*.theme.properties` files, read the
last used theme from preferences, and load that theme which includes setting the Look and Feel.


## Loading a Theme


Loading a theme consists of two main operations: loading the Look and Feel and building the
set of values for all defined resource IDs.


## Loading the Look and Feel


Because each Look and Feel presents different challenges to the theming feature, there is a
`LookandFeelManager` for each Look and Feel. The `LookandFeelManager` is
responsible for installing
the Look and Feel (in the case of Nimbus, we had to install a special subclass of the
`NimbusLookandFeel`), extracting the Java resources mappings (Java Look and Feel
objects also use a resource ID concept), group the Java resources into common groups, possibly
fix up some issues specific to that Look and Feel, possibly install global properties, and have
specific update  techniques to get that Look and Feel to update its component UIs when
values change.


## Creating the Active Theme Values


After the Look and Feel is loaded and the Java values extracted, the final resource mapping is
created. This is done by loading various resource values sets (each stored in a GThemeValueMap)
in the correct order into a new `GThemeValueMap` in `ThemeManager` called
"currentValues" . When values are loaded into a `GThemeValueMap`, they will replace
any existing values with the same ID. The values are loaded in the following order:


- Java defaults (values from Look and Feel)
- application defaults (from \*.theme.properties files)
- applications dark defaults (if theme is dark)
- theme values (values that were overridden by a specific theme)


## Changing Values Associated With Resource Ids


Whenever the value associated with a resource ID changes, the application gets notified in
various ways to update the display with the new value. The technique used to notify the
application differs depending on the resource type and the Look and Feel (these differences are
captured in the `LookandFeelManager` sub-classes for each Look and Feel). It can also
vary depending on whether the value is an application defined resource or a Java defined
resource.


### Updating Colors


Updating Colors is the easiest of all the resource types. First
`GColor.refreshAll()` is called,
which causes every `GColor` to refresh its internal delegate `Color`.
This is the purpose of using the `GColor` class, to introduce a level of indirection
that allows us to change runtime behavior without having to recompile.
Next, `repaint()` is called on all the top-level Java windows in the application.
Also, since color values in the `UIDefaults` are actually
replaced with GColor objects, this technique works for both application defined resources and
Java defined resources.


### Updating Icons


Updating icons is a mixed bag. If the icon is application defined,
`GIcon.refreshAll()` is
called which causes every `GIcon` to refresh its internal delegate icon and then
call `repaint()` on all the
windows. If the icon is Java defined, then the `UIDefaults` has to be updated and the
`updateComponentTreeUI()` method on all windows is called.


### Updating Fonts


Updating Fonts is a bit more involved than updating colors and icons, due to the inability
to use the indirection model when working with fonts. First, if the changed font is Java
defined, the `UIDefaults` for that font ID (and any that derive from it) are updated.
Next, all the components that have called `Gui.registeredFont()` are updated. (The
registration system for fonts is what allows us to notify components of updates, since fonts
cannot use the indirection model.)
Finally, the `updateComponentTreeUI()` method is
called on all windows in the application.


## Creating/Editing/Saving Themes


New themes can be created and saved to files in the theme directory in the user's
settings directory (`<user settings>/themes`).
When the application is started, this directory is scanned and any
`*.theme` files are loaded and available to be selected as the active theme.
The `Gui` class has
methods for setting the value of a color, font, or icon for a given resource ID. If any values
are currently different from the active theme, the theme can be saved. If the active theme is a
built-in theme, then the only choice is to save using a new theme name. Saving the
theme will create a new "xyz.theme" file where "xyz" is the name of the theme. Otherwise, the
existing theme file can be overwritten or a new theme name can be supplied to save to a new
file.


## External Icons


When setting icons for an icon resource ID, the user has the option of using an icon that
exists in the application (on the classpath) or using any supported icon file (.png or .gif) on
the filesystem.  If the user
chooses to use a non-application icon file, then that icon will be copied into an images
directory in their application directory. These icons are considered external in that if the
theme were given to another user, you would also need to give them these icon files, as they
will not exist in other application installations.


## Importing/Exporting Themes


Themes can be shared with other users by exporting and importing themes. When exporting a
theme that doesn't use any external icons (icons not on the classpath), the theme can be
exported to a `.theme` file of the user's choosing. If the theme does contain
external icons, the
user has the option to save the theme as a .zip file, which would contain both the .theme file
and all the external icon files.


## Look and Feel Notes


Getting the theming feature to work on all the various Java Look and Feels is a
challenge. Java created the concept of `UIDefaults`, which is a mapping of property
names
to values. The implication is that users can change Look and Feel settings by changing values
in the `UIDefaults`. Unfortunately, not all Look and Feels support this concept.
Nimbus and GTK+, in particular are problematic. Nimbus somewhat honors values in
`UIDefaults`, but only if those values are
installed before Nimbus is loaded. So for our theming purposes, we had to extend the Nimbus
Look and Feel in order to override the `getDefaults()` method (this is the method
where Look and Feels populate the `UIDefaults`) so that we can install any overridden
values from the selected theme. Also, since Nimbus does not respect changes to these values after
they have been created, every time a Java defined property changes, we have to re-install the
Nimbus Look and Feel.  The GTK+ Look and Feel is even more problematic. It gets many of its
properties
from native libraries and there doesn't appear to be anyway of changing them. Therefore, themes
based on GTK+ doesn't allow for changing Java defined values. To compensate for the
differences among Look and Feels, we created a `LookandFeelManager` base class with
sub-classes for each Look and Feel.


Provided by: *Theme Manager*


**Related Topics:**


- [Theming Overview](ThemingOverview.md)
- [Theming User's Guide](ThemingUserDocs.md)
- [Theming Developer's Guide](ThemingDeveloperDocs.md)


---

[← Previous: Developer's Guide](ThemingDeveloperDocs.md) | [Next: Appendix →](../Misc/Appendix.md)
