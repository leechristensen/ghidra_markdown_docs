# Developer's Guide to Theming


This document provides information an application developer should know when developing
plugins, actions, scripts, etc., that use colors, fonts, or icons. By following these guidelines,
developers can easily make use of Ghidra's theming capabilities.


> **Tip:** Most classes referenced in this document
live in the generic.theme package.


## Theme Resource Types


When developing application code for Ghidra such as plugins, actions, etc., developers often
want to use colors, fonts, and icons. The key idea to support theming is to never
**directly**
reference those resources. Instead, the developer should create an ID string for the resource
and then in a `module.theme.properties` file, provide a default value for that
ID. (Also, you may define an alternate "dark" default value that will be used if the
current theme is considered a dark theme).  The way you
define and use these IDs is a bit different depending on whether the resource is a color, font,
or icon. Colors and icons are similar in that developers use these types by creating either
`GColor` or `GIcon`.
Unfortunately, because of the way fonts are implemented, there is no equivalent
`GFont`, so using fonts is a bit more involved.


### Colors


For colors, developers should use the `GColor` class. Simply construct a new
`GColor` object passing in the color resource ID as the argument.
`GColor` is a subclass of `Color`, so it can be
used anywhere a `Color` would be used. The developer then needs to provide a
default value for that ID in the module's `module.theme.properties` file.
So, for example:


`panel.setBackground(Color.Red);`


becomes


`panel.setBackground(new GColor("color.bg.abc"));`


and


`public static final Color MY_COLOR = Color.BLUE;`


becomes


`public static final Color MY_COLOR = new
GColor("color.fg.xzy");`


The `GColor` class uses a delegation model where all method calls to
`GColor` get mapped to
its delegate color. If ever the color associated with a `GColor`'s resource ID
changes, the `GColor` is automatically updated by calling the
`refresh()` method.  This is done whenever the
`Gui.setColor(id)` is called or a new theme is loaded.


### Icons


Icons work just like colors, so you can just create a `GIcon(String id)`.
So, for example,


`public static final Icon MY_ICON =
ResourceManager("images/balloon.png");`


becomes


`public static final Icon MY_ICON = new
GIcon("icon.text.bubble");`


### Fonts


Unfortunately, fonts are unable to use the delegation model used for colors and icons.
Therefore, there is no `GFont` class. Programming fonts requires a bit more work.
If a font used directly, such as in renderer or in a paint method, simply get the
font each time
from the `Gui` class, as shown below. To set a font on a component, use
`Gui.registerFont(Component, String)`. Once the component is registered, the
application will
automatically update the component if the font associated with that ID changes. So, for
example:


`Font font = new Font("Monospaced", Font.BOLD, 12);`


becomes


`Font font = Gui.getFont("font.xyz");`


or


`myLabel.setFont(new Font("Dialog", Font.PLAIN, 14)`


becomes


`Gui.registerFont(myLabel, "font.xyz");`


### Font Usage in Tables, Lists and Custom Painting


Ghidra makes great use of tables and to a lesser extent, lists.  Both tables and lists
use renderers to paint cell values.


- Java - By default, Java will use the font of the table/list as the font used during rendering.
- Ghidra Tables - Ghidra does <u>not</u> use the table's font for rendering by default.  Instead,
the renderer is initialized with the fonts used by `JLabel`, with additional
fonts for bold and monospaced text.
- Ghidra Lists - Ghidra does not currently use custom rendering for lists.  Thus, list cell
rendering will make use of the list's font, which is Java's default behavior.


We point out this difference between Java and Ghidra here so that developers understand
that changing fonts used for tables differs from Java.   Specifically, calling



```

     table.setFont(newFont);

```


will not affect the font used when rendering the table.  To programmatically change the
fonts used for tables, you can set the font directly on each cell renderer.  As with a
any custom fonts used, be sure to define theme properties file and register then with the
Gui class as outlined above.


The fonts used for any painting operations, including table and list cell rendering, as well
as any code that overrides `paint` will work correctly within the theming
environment as long as the fonts are derived from the default Look and Feel values or are
obtained from the `Gui` class.  In other words, as long as the
fonts used in custom painting are not hard-coded, any changes to the fonts via the theming
API will appear on the next call to paint the UI.


## Resource ID Strings


Resource IDs are strings used to identify a color, font, or icon. These strings are
created by the developer and should be chosen in a way that it is as self-describing as
possible. So, for example, if you wanted the text color in some error message in some widget
"abc", you might create the color ID "color.fg.abc.error". To help keep resource IDs
consistent, we created a convention for IDs as follows:


```

     [type].[category[...]].[client].[specialized uses]

```


- **type:** color, font, or icon.
- **category:** any value, examples include 'bg'(background), 'fg'(foreground),
'cursor'. There may be multiple dot-separated values.
- **client:** the plugin name or feature name.
- **specialized uses:** any key value here that applies to the client, such as
'vertex' for a graph client.


Examples:


- color.bg
- color.bg.listing
- color.bg.functiongraph.vertex.group
- font.listing
- font.listing.header
- icon.error
- icon.delete
- icon.plugin.byteviewer.provider


- <a name="system-ids"></a>**System IDs:** The following resource IDs are created and
used by the system.  For a description of how these IDs are used internally by the
application, see the `UiDefaultsMapper` class .   The `system.*` keys
allow users to quickly change many Look and Feel values via these high-level concepts.   The
`laf.*` properties are for internal use and do not need to be changed by the user.
A description of the system properties can be found in the `SystemThemeIds` class.


- laf.color.*
- laf.font.*
- laf.icon.*


- system.color.*
- system.font.*


The `system` property names use the standard property names, such as `
font, bg` and `fg`.  These properties introduce these additional terms:
`control, view, menu and tooltip`.   `control` refers to items that
generally control the state of the application, such as buttons and check boxes.
`view` refers to widgets that display data, such as trees, tables and text
fields.  `menu` and `tooltip` work with the items after which they are
named.


## Theme Property Files


The default values for resource IDs are defined in files that reside
a module's data directory (not all modules define this file).   These files all
are named to end in `theme.properties` and begin with the module's name.   Some
modules make use of multiple files in order to better manage the volume of IDs.   In this
case, the name of each properties file offers a clue as to its contents.  Thus, for small
modules, those without many resource IDs in use, one theme properties file is sufficient to
easily define and manage all required IDs.  But, we recommend larger modules use multiple
files, one for each sub-feature. The application will find all theme property files as long as
they exist in a module's data directory and are named with the
`.theme.properties` suffix.


### Theme Properties File Naming Convention


To promote consistency, theme property files should use the following naming
convention:


```

      module name[.additional name]].theme.properties

```


Examples:


- base.theme.properties
- base.listing.theme.properties


### Theme Properties File Format


Theme files uses a very simple format for specifying theme property values. Each line
specifies a property ID (sometimes referred to as the key) and a value, separated by an
"=". A theme properties file consists of two sections: the standard defaults section and a
section for specifying defaults for "dark" themes.


`

[Defaults]

[property id 1] = [some value]
[property id 2] = [some value]
[property id 3] = [some value]
...

[Dark Defaults]

[property id 1] = [some value]
[property id 2] = [some value]
...

`


Example:


```

[Defaults]

color.bg = white
color.bg.listing = color.bg

color.fg.listing.address = black
color.fg.listing.bytes = #00ff00

font.global = courier-BOLD-12
font.global.listing = font.global

icon.error = defaultError.png


[Dark Defaults]

color.bg = black

color.fg.listing.address = gray
color.fg.listing.bytes = orange

```


NOTE: The `[Dark Defaults]` section is for <u>optionally</u> overriding values
defined in the standard `[Defaults]` section. If a property ID is not given a value
in the defaults section, it is an error. If a value is not defined in the
`[Dark Defaults]` section, then the value defined in the `[Defaults]`
section will be used in a dark theme.


## Theme Property Values


The values specified in the theme properties files can be specified in a variety of ways,
including ways to modify other property values. For example, an icon's size can be modified
directly in the theme properties file. A font value can specified as a reference to another
defined font, but with a different size or style.


Also, any value can also be a reference to some other ID of the same type. So, for
example, a reference color entry might be something like "color.bg.listing = color.bg". This
says that the listing's background color should be whatever "color.bg" is defined to be. Note
that all of the application's defined properties start with either "color.", "font.", or
"icon.".



Properties defined by the theming system do not follow this pattern. To reference a
property that does not have a standard prefix, an ID can be prefixed with `[color]
`, `[font]`, or `[icon]` as appropriate to allow the theme
property parser to recognize the values as IDs to other properties. For example, to refer to a
system property named `system.color.bg.view`,
you would use the following definition:


`color.bg.tree = [color]system.color.bg.view`


### Color Values


Color values supports the following formats:


- #rrggbb
- #rrggbbaa
- 0xrrggbb
- 0xrrggbbaa
- rgb(red, green, blue)
- rgba(red, green, blue, alpha)
- *web color name* // the case-insensitive name of a web color such as red, olive,
or purple


Examples:


```

        color.foo = #0000ff             // blue
        color.foo = #ff000080           // red with half transparency
        color.foo = 0x00ff00            // green
        color.foo = 0xff000080          // red with half transparency
        color.foo = rgb(0, 0, 255)      // blue
        color.foo = rgba(255,0, 0, 128) // red with half transparency
        color.foo = blue                // web color defined as 0x0000FF
        color.foo = LawnGreen           // web color defined as 0x7CFC00

```


### Font Values


Font values are specified using the following format:


```

      family name-style-size

```


- family name: the font name such as `monospaced`, `dialog`,
`courier`.
- style: One of `PLAIN`, `BOLD`, `ITALIC`, or
`BOLDITALIC`.
- size: the font point size. 12 is very common.


Examples:


```

        font.foo = monospaced-PLAIN-12
        font.foo = courier-BOLD-14
        font.foo = SansSerif-ITALIC-10

```


#### Font Modifiers


When referencing another font, the referenced font can be modified using the following
format:


```

      font.ref[family name][style][size]

```


- *font.ref*: the theme property ID of some other font
- family name: use the size and style of the reference font, but use this font
family.
- style: use the same font as the reference font, but with this style. One of
`PLAIN`, `BOLD`, `ITALIC`, or
`BOLDITALIC`.
- size: use the same font as the reference font, but with this size.


Examples:


```

        font.foo = SansSerif-PLAIN-12   // standard font spec
        font.bar = font.foo[BOLD]       // results in SansSerif-BOLD-12
        font.bar = font.foo[15]         // results in SansSerif-PLAIN-15
        font.bar = font.foo[monospaced] // results in monospaced-PLAIN-12
        font.bar = font.foo[ITALIC][15] // results in SansSerif-ITALIC-15

```


### Icon Values


Icon are specified by simply entering the name of an icon that is in the classpath.
However, an icon value can get complicated because it can be modified in a number of ways,
such as scaling, disabling, even overlaying other icons. The format is as follows:


```

      iconName[size(width,height)][disabled]{overlayIconName[size(width,height)[disabled][move(x,y)]}{...}


```


- *iconName*: the name the base icon
- size(width,height): optional modifier to scale the image to the given size.
- disabled: optional modifier to create a disabled version of the icon.
- {...}: optional modifier to overlay an icon on the base icon. It is recursively
defined using the standard icon format.
- move(x,y): optional modifier on overlays to position them relative to the base
icon.


Examples:


```

        icon.foo = house.png               // using the icon house.png found as an image resource on the classpath
        icon.foo = house.png[size(10,10)]  // uses the house.png icon, but scales it to 10x10
        icon.foo = house.png[disabled]     // creates a disabled version of house.png
        icon.foo = house.png[16,16]{hammer.png[size(4,4)][move(12,12)]}
                                                // creates a 16x16 version of the house icon with a 4x4 scaled
                                                // hammer.icon overlayed in its lower right corner

```


To create stand-alone icon suitable for dynamically overlaying other icons, there is
special syntax for specifying an empty base icon.  Use the empty icon along with another
overlay icon in some specific area of the empty icon to create a final icon that can be used
as an overlay for other icons. For example, to
create an overlay icon that would add a flag to the bottom-right corner of any other icon:


```

        icon.overlay.flag = EMPTY_ICON[size(16,16)]{flag.png[size(6,6)][move(10,10)]}

```


## Useful Concepts


### GThemeDefaults


This class contains many common application theme values for developers to use, such as
the default background color.   These values can be used directly so developers do not have
to instantiate theme objects using theme IDs.


### Icons


When adding icons to the application, consider using standard icons provided by the
`Icons` class.   Many generic concepts that require icons are in this class.


### Palette Colors


A list of palette colors has been defined in `gui.palette.theme.properties`.
These palette colors values are meant to be used by developers to reduce the total number
of colors used in the application.   These color ids and values are viewable in the
[Theme Editor Dialog](ThemingUserDocs.md#theme-editor-dialog).


One of the benefits of using the palette system is that it is easy for end-users to change
one palette color to update all widgets in the application.


We recommend you use the existing palette colors when picking colors for your widgets.


### HTML Foreground Colors in Messages


Some developers use HTML messages in labels, tables, tooltips, and in calls to system APIs,
like `Msg`.   Using HTML text allows clients to control the formatting of the
text, including the usage of color.  If you use color in your HTML, then we suggest you do
so using GColors, like this:


```

    String message = "Some text: <FONT COLOR=\"" + Messages.ERROR + "\">" + errorText + "";

```


In this example, an HTML message is created and part of that text is colored with the
standard error message color, which is red in a light mode theme.	You can also use your
own `GColor` object in your HTML messages.  Using standard system colors or
GColors allows these colors to be updated as the theme changes.  We do not
recommend the use of hard-coded color values.


### Options Usage of Colors and Fonts


The `Options` class in Ghidra facilitates user-configurable options in the
application.   Previously, developers could use options to allow end-users to control color
values.  In the new theme-based system, all colors are controlled via theming.  However, to
make the transition to theming easier for developers, we added methods to the options class
that allow the developer to bind color editing via the options UI.  These color options will
write any changes directly to the theme system.


See: `Options.registerThemeColorBinding()` and
`Options.registerThemeFontBinding()`


### UiDefaultsMapper


This class discusses some of the plumbing the application uses to unify the various Look
and Feel concepts presented by the different LaFs.


### SystemThemeIds


This class is used by the `UiDefaultsMapper` class and presents a set of resource IDs common across all
LaFs. These values can be changed by the user.   See also the description of
<a name="system-ids"></a>System IDs in this document.


### Known Issues


Sometimes switching between themes does not reset all widgets.  When
this happens, you may notice odd UI artifacts.  These will go away when the application is
restarted and often when you again switch the theme.


*Provided by: *Theme Manager**


**Related Topics:**


- [Theming Overview](ThemingOverview.md)
- [Theming User's Guide](ThemingUserDocs.md)
- [Theming Architecture](ThemingInternals.md)
