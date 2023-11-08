## Show Info about Template
It is run when prompt: <template> -i (info)
It displays template metadata is exist and the test_template if exist otherwise displays the actual template
Then it prompts with the selected template as default


InteractiveTemplateRenderer
It selects a template for rendering. 
Default action is render template
Provides other actions which help to find the right template (e.g. info, edit, doc)

It prompts the templates to the user. It captures the user input and it sends it to the input parser (input processor) which in turn calls the appropiate action

TemplateRendererShell
It captures user input while provide suggestions both both templates and parameters
It keeps a queue of prompts


RenderTemplateAction
It checks if the temp
It runs render template by default



It displays a list of templates to the user
InteractiveActionPicker
ActionShell
It displays a list of actions to the user with suggestions 
Take a list of Actions, where each action has handler

RenderTemplateAction()




A shell have a lists of actions and each action can have args
A shell displays the list of actions when the user types in and it also suggest the possible args for each action 

A `RenderLibraryTemplateShell`, takes a library of templates and it creates a list of render actions for each of them.
It a shell that points to a template library and it has one `ProcessTemplateAction` action for each template within the library

A `ProcessTemplateAction`, parses input and if the input matches the template relative path renders the template. 
A template action runs and it prompts again

Input string is parsed into action
An action runs
