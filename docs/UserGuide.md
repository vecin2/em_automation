# User Guide

- [Main Commands](#main-commands)
- [Key Mappings](#key-mappings)
  - [Select Template](#select-template)
  - [Prompt](#prompt)
  - [Entering template values](#entering-template-values)
- [Commands](#commands)
  - [print-sql](#print-sql)
  - [run-sql](#run-sql)
  - [create-sql](#create-sql)
    - [update.sequence](#updatesequence)
  - [test-sql](#test-sql)
    - [test-sql While Creating a Template](#test-sql-while-creating-a-template)
    - [test-sql While Refactoring a Template](#test-sql-while-refactoring-a-template)
    - [test-sql During Installation](#test-sql-during-installation)
- [Searching for Templates](#searching-for-templates)
  - [Example: Add Activity To Perspective](#example--add-activity-to-perspective)
  - [Searching Using Action Names](#searching-using-action-names)
  - [Searching Using By Reversed Engineering](#searching-using-by-reversed-engineering)
- [Logging](#logging)

## Main Commands

They are three main use cases: [print-sql](#print-sql), [run-sql](#run-sql), or [create-sql](#create-sql). The application flow across all of three is very similar:

- Run the command by running `sqltask <command_name>`
- Application prompt user to [select a template](#searching-for-templates) from all the templates available on the current [library](pointtoreadmelibrary)
- Application prompts user to enter values to replace template placeholders
- Once all the template values are entered, application asks to select another template again. User can continue generating SQL by selecting another template (SQL will be appended) or, or he can select "x. Save && Exit" to end the SQL generation and runs the appropriate action, whether is [print-sql](#print-sql), [run-sql](#run-sql), or [create-sql](#create-sql)

## Controls

#### Select Template
The select menu can take a few parameters that will display different information about the template
- \<template_name\>: proceeds to generate SQL for the selected template
- \<template_name\> **-t**: if exist, it prints out the test associated to this template which allows the user to see an example of the SQL generated by this template.
- \<template_name\> **-h**: if exists, it prints out the [description](linktodescription) message for this template.
- \<template_name\> **-hh**: if exists, it opens the [documentation](linktodescription) for this template on web browser.

#### Prompts
The following controls is applicable for any prompts: 
- Ctrl + n: Navigate to the "next" option within a list of suggestions.
- Ctrl + p: Navigate to the "previous" option within a list of suggestions.
- TAB: pops up a list of suggestion if there is one or navigate to the next one if the list is already displayed.
- Shift + TAB: Navigate to the previous option within a list of suggestions.
- Ctrl + w: Removes the previous word that was typed.

#### Entering template values
During prompts when filling template placeholders:
- "<": the application goes back and prompts the previous value. Useful if an incorrect value was entered.

## Commands

### print-sql

This command prints out the final SQL to the console. To be used,  for example, while writing a new template, or to copy and paste the generated SQL from the console.

### run-sql

This command is similar to [print-sql](#print-sql) except that instead of printing to console it runs the generated SQL against the [configured database](#configured-database).

SQL templates typically use relatives IDs, e.g. `@PROFILE.SYSTEMADMIN`. This command, it parses these relative IDs and replace them with real IDs found on `CCADMIN_VERSION` table before it can run the final SQL against the database.

### create-sql

This commands asks for SQL module name, and task name, and then using those values and the [database release version](#database-release-version) it creates the `tableData.sql` and [update.sequence](#update.sequence) files under the right project location.

For example, if database release version is currently "R_01"
user enters "EnvLocal" as SQL module name, and "extendCustomerInlineSearch" as a task name, this command creates the files under:
<<project_home>>/modules/**EnvLocal**/sqlScripts/oracle/updates/**R_01**/**extendCustomerInlineSearch**

#### Database Release Version
`sqtask` computes the current version from the `releases.xml` file on the current project.
This value can be overridden by setting the property `db.release.version` on the [core.properties](blabalb) file.

#### update.sequence

If the project is using SVN and, SVN is installed with command line tools, the application calls `svn info` to get the latest revision number to compute the update sequence number.

For example if the latest revision number is 10, and this command runs it creates `update.sequence` file with this content: `PROJECT $Revision: 11`

The property `svn.rev.no.offset`  can be set [core.properties](blabalb) file in an scenario, where the latest revision number does not align with the update sequence number, for example if the project is moved to a different SVN server. 
If `svn.rev.no.offset=100` and current revision number is 300, the next update sequence will be `401` instead of `301`.

### test-sql

This command runs all the tests found under `test_templates` folder within the configured [library](blabalb). 
Each test checks that the SQL is generated as expected and that it runs successfully against the database.

#### Test While Creating New Templates
It is very useful while creating templates, users can create the test by copying the final SQL from some existing project and then start introducing placeholders and run the test frequently to make sure the generated SQL remains as expected. In this scenario is useful to run one single test instead of the full test suite:

`sqltask test-sql --test-name test_add_entity_definition.sql`

#### Test While Refactoring Templates

It is also very useful when refactoring templates. For example, we are creating a "add_entity_definition.sql" template, which also also inserts into "LOCALISED_FIELD" table. Initially, all the SQL is written within the same file. Later, we decide to extract "LOCALISED_FIELD" into it's own template since it is also used by other templates. We can do this using the [include tag](#include) on the the original template. Having a test makes easier to do this kind of changes while guaranteeing that the final SQL does not change.

#### Test During Installation

It is advice to run this command as part of the initial installation, to make sure all the tests are still running. For example, a test could fail because we are using a different product version, or the project database is different from the one used when writing the template (oracle vs SQL server)

## Searching for Templates

Finding what template applies to a specific task is key.
The application uses a fuzzy searcher to match user input against the template available on the [library](libray). Templates are named after what the template does and they can have long descriptive names so they are easier to find.

### Fuzzy Search Example

A user wants to create SQL to configure agent desktop to show a new static verb on the home perspective. An existing template for this is called [add_activity_to_perspective](blabla). If the user types *"acti"*, the fuzzy searcher shows all the templates matching that input like the following:
- add**acti**vity_to_perspective.sql 
- remove**acti**vity_from_perspective.sql 
- **a**dd_asso**c**ia**ti**on_type
- add_b**a**si**c**\_en**ti**ty_definition'.

This works great as long as the user knows that verbs on the left hand side with the word "activities" 

However, he might refer to this use case as "adding verbs to context". Then he starts typing "verb" and he is prompted with unrelated templates e.g. "add_verb_to_entity".
This is why it is importatn how the templates are named, and it is reponsability of the library to choose appropiate names and to define name conventions that help finding templates quickly. 

The existing [SQL task library](sdffd) defines naming rules [here](dabl)


So how can a user find the right template, specially, when he haven't use it before? Although there is no an straight answer the following can help.

### Searching By Entity Names
<details>
<summary>Click me</summary>
  
  ### Heading
  1. Foo
  2. Bar
     * Baz
     * Qux
    
</details>


<details>
<summary>TITLE</summary>

BODY CONTENT

</details>

<ol>
<li> <details><summary>Hello</summary><blockquote>
  <details><summary>World</summary><blockquote>
    :smile:
  </blockquote></details>
</blockquote></details>
</li>
</ol>


### Searching By Action Names

Templates are named behind the action they accomplish. The following actions are currently implemented: "Add", "Remove", "Update", "View" or "Extend".
Avoid using other synonyms like "Insert", "Create", "Delete", "Display", etc...

For example in the above example user should type "add" to get all the templates that are adding something into the system and then navigate through the list to find the one he needs (add_activity_to_perspective.sql).
You can see a list of templates categorized by action here.

### Searching By Reversed Engineering

This is the least prefer option, but before giving up and writing your own SQL it worths exploring it. 
The approach is often used in projects, when the developer knows that a certain SQLTask touches a specific database table.
For example, a user wants to add a verb to an entity and he knows that "EVA_VERB" is one of tables involved. Searching for the term "EVA_VERB" with a search tool pointing to the templates folder will retrieve all the templates that touch this table. Then, from the template name it should be possible to identify which template to use.



## Logging

The application logging is configured by default to write to the logs dir within the main application folder.
Logging configuration can be modified by creating a file called `logging.yaml` under the app config folder.
This is a example of a valid configuration file:

```yaml
version: 1
disable_existing_loggers: False
formatters:
  simple:
    format: '%(asctime)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: simple
    stream: ext://sys.stdout

  info_file_handler:
    class: sql_gen.log.handlers.MakeRotatingFileHandler
    level: INFO
    formatter: simple
    filename: information.log
    maxBytes: 10485760 # 10MB
    backupCount: 20
    encoding: utf8
loggers:
  app_logger:
    level: INFO
    handlers: [console, info_file_handler]
    propagate: no
root:
  level: INFO
  handlers: [info_file_handler]
```