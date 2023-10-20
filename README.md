[library]: https://github.com/vecin2/sqltask-templates

![img](docs/example.gif)

## sqltask
A command line SQL generator for Agent Desktop and KM projects.

Overriding a verb, extending an entity, or creating and assigning entitlements are just some examples of tasks that required SQL scripts. The list of tasks is very large and it keeps growing as the product becomes more configurable which makes it very difficult to keep track of them. 

Currently, developers builds this SQL by searching through product scripts or on previous projects to find a similar example that they can use as template, most of the SQL is reused and some values are replaced. Many of these values are usually relatives IDs and developers need to run multiple database queries to compute them. This way, tasks that involve large amount SQL like, creating a new KM content type, can be pretty tedious. It is also hard to find examples of SQL tasks that are less common, and developers have to reverse engineering in order to work out the SQL. After all this work, the script is buried into a project repository with limited visibility to other developers.

`sqltask` is based on this idea of using previous scripts as templates. It uses a [library] of SQL tasks, where each task is implemented as a template, which is basically a SQL file with placeholders for those values that would typically changed. These templates are kept under version control in SQL task so other developers could contribute to grow the library. 

`sqltask` uses fuzzy searching to help finding a specific template within the library. Then, it parses the template to extract the placeholders and it prompts them to the user with suggestions to avoid from having to make extra database queries.

## Table Of Contents

- [sqltask](#sqltask)
- [Table Of Contents](#table-of-contents)
- [User installation](#user-installation)
  * [Library](#library)
  * [Windows Executable](#windows-executable)
  * [Configuration](#configuration)
  * [Database Client](#database-client)
    + [Oracle Client](#oracle-client)
- [Test Installation: First Run](#test-installation--first-run)
  * [Run Tests](#run-tests)
- [Hello World](#hello-world)
- [User Guide](#user-guide)
- [Designer Guide](#designer-guide)
- [Developer Guide](#developer-guide)


## User installation

### Library
Clone the SQL task [library] into a folder within your filesystem.  When choosing the folder please consider that the same library could serve multiple projects so it make sense to keep it out of an specific project, so use  a general location like  `c:\em\sqltask-library`.

This path will be used when configuring the project on the [configuration](#configuration) step, 

### Windows Executable
Download [sqltask.exe](releases) and save it in any location present within the `%PATH%` environment variable - it could be an existing location or create new one, for example `C:\em\bin`

Verify that this works by running `sqltask.exe` from the root folder of your project or any subfolder, a help message should be printed out.
 
### Configuration
Open the command line, navigate to a folder inside the project and run `sqltask init`. Follow the instructions on the screen.  Configuration settings are written to `<<project.home>>/project/sqltask/config/core.properties` and they commit to version control and shared between developers within that project.

Library path is written to a `<<project.home>>/project/sqltask/config/.library`. This file is meant to be added to `.gitignore` as the library path could be different for each developer.

Settings can be adjusted by running the `init` command again or  by directly editing the files:
- `<<project.home>>/project/sqltask/config/.library`
- `<<project.home>>/project/sqltask/config/core.properties`



### Database Client

`sqltask` connects to a database and therefore requires a database client to be installed. This could be oracle or SQL server depending on the project.

#### Oracle Client
*If your local machine already has an oracle database installed and available within `%PATH%` this step could be skipped.*

On the [downloads](https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html) section of the oracle web site, find the package matching the project's database version and download the appropriate "Basic Light Package". For example if your project has oracle 19, download the latest oracle 19 `Basic Light Package` which, at the time of this writing, is `instantclient-basiclite-windows.x64-19.18.0.0.0dbru.zip`.

Unzip it to a folder in your filesystem, for example : `C:\Oracle\instantclient_19_18`

Add this path to the `%PATH%` within your user environment variables

## Test Installation: First Run

Open the command line and navigate to a folder within an your project:
- Run `sqltask.exe print-sql` it should start the application and prompt for a template name.
- Start typing the name. It should trigger the fuzzy searcher and bring up a list of templates matching the input entered.
- Select a template and hit `<Enter>`. At this point the application looks for configuration under `work/config/show-config-txt` and, if it doesn't find it, runs   `ccadmin show-config -Dformat=txt`, which is required to get the project's configuration including database connections details.
- Enter the values to fill the template's placeholders
- After all the values are entered, select template menu is displayed again.
- You can select another template or  `x. Save && Exit` to finish. 
- The rendered SQL should be printed.

Finally you can also run [sqltask.exe test-sql](docs/UserGuide.md#test-sql) to check that the templates are still valid for the current product version

## Adding a new Template

Create a `hello_world.sql` file under `<<sqtask.library.path>>/templates` folder with the following content: `Hello {{ name }}!`
Run `sqltask print-sql` and select the template `hello_world.sql`.
You should see `name` being prompted. Enter a value and press enter.
Finally type 'x' to save and exit. 
You should see the generated template printed on the console.

## User Guide

For details on how to use the tool and the specific commands  please refer to the [user guide](docs/UserGuide.md).

## Designer Guide

For details on how to write new templates please refer to the [designer guide](docs/TemplateDesignerGuide.md).

## Developer Guide

For details on how to make changes to the this tool refer to the [developer guide](docs/DeveloperGuide.md).
