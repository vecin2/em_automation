---


---

<p><img src="https://raw.githubusercontent.com/vecin2/em_automation/master/docs/rewiring_verb.gif" alt="img"></p>
<h1 id="sqltask---an-sql-generator-for-em-projects">sqltask - an sql generator for EM projects</h1>
<p>sqltask is command line application that helps users generating SQL scripts. Each script is created as a template, sqltask then parse th template to identify the diferent variables and it prompts them to the user. Once all the variables are entered it renders the template and sends the result to the corresponding output.</p>
<p>Templates are written using <a href="http://jinja.pocoo.org/">jinja templates syntax</a>  and they should be designed in a way that they provide enough information to users when filling template values, and they should minimize user interactions, avoiding asking for values that could be computed.</p>
<h1 id="table-of-contents">Table Of Contents</h1>
<ul>
<li><a href="#sqltask---an-sql-generator-for-em-projects">sqltask - a sql generator for EM projects</a></li>
<li><a href="#table-of-contents">Table Of Contents</a></li>
<li><a href="#basic-usage">Basic Usage</a>
<ul>
<li><a href="#creating--a-sql-task">Creating  a SQL Task</a></li>
<li><a href="#exiting-the-application">Exiting the application</a></li>
<li><a href="#show-help">Show help</a></li>
<li><a href="#adding-new-templates">Adding New Templates</a>
<ul>
<li><a href="#hidding-a-template">Hidding a Template</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="#user-installation">User installation</a>
<ul>
<li><a href="#windows-console-tools">Windows Console Tools</a></li>
</ul>
</li>
<li><a href="#template-design">Template Design</a>
<ul>
<li><a href="#filters">Filters</a>
<ul>
<li><a href="#concatenate-multiple-filters">Concatenate multiple filters</a></li>
<li><a href="#list-of-builtin-filters">List of Builtin filters</a></li>
</ul>
</li>
<li><a href="#global-functions">Global Functions</a></li>
<li><a href="#list-of-global-functions">List of Global Functions</a></li>
<li><a href="#string-python-builtin-functions">String Python Builtin Functions</a></li>
<li><a href="#fomatting-and-naming-convention">Fomatting and Naming Convention</a>
<ul>
<li><a href="#inserts">Inserts</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="#build-extensions">Build Extensions</a>
<ul>
<li><a href="#developer-setup">Developer Setup</a>
<ul>
<li><a href="#running-tests">Running tests</a></li>
</ul>
</li>
<li><a href="#imlementing-new-global-functions">Imlementing new Global functions</a></li>
<li><a href="#implementing-new--filters">Implementing new  Filters</a></li>
</ul>
</li>
</ul>
<h1 id="basic-usage">Basic Usage</h1>
<p>This section run through the steps of generating a SQL script:</p>
<ul>
<li><a href="#adding-new-templates">Add a new template</a> called <code>change_verb_context2.sql</code>:</li>
</ul>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token keyword">UPDATE</span> EVA_CONTEXT_VERB_ENTRY
<span class="token keyword">SET</span> <span class="token punctuation">(</span>CONFIG_ID<span class="token punctuation">)</span><span class="token operator">=</span> <span class="token punctuation">(</span><span class="token variable">@CC.</span>{{new_config_id <span class="token operator">|</span> description<span class="token punctuation">(</span><span class="token string">"new_config_id (e.g. Home, CustomerPostIdentify, ...)"</span><span class="token punctuation">)</span>}}<span class="token punctuation">)</span>
<span class="token keyword">where</span> CONFIG_ID <span class="token operator">=</span> <span class="token variable">@CC.</span>{{old_config_id} <span class="token operator">|</span> <span class="token keyword">default</span><span class="token punctuation">(</span><span class="token string">"NULL"</span><span class="token punctuation">)</span>}
<span class="token operator">and</span> VERB <span class="token operator">=</span> <span class="token string">'{{verb_name}} '</span><span class="token punctuation">;</span>
</code></pre>
<ul>
<li>Run the application by simply typing <code>sqltask</code> in the comand line. The new template should show as one of the options.</li>
<li>Select the template, and starting filling the values as they are prompted:</li>
</ul>
<pre class=" language-bash"><code class="prism  language-bash">	new_config_id <span class="token punctuation">(</span>e.g. Home, CustomerPostIdentify, <span class="token punctuation">..</span>.<span class="token punctuation">)</span>: 
	old_config_id <span class="token punctuation">(</span>default is NULL<span class="token punctuation">)</span>: 
	verb_name: 
</code></pre>
<ul>
<li>Assuming <code>Customer</code>, <code>Home</code> and <code>indentifyCustomer</code> are entered as values the template will be render and printed out as following:</li>
</ul>
<pre class=" language-sql"><code class="prism  language-sql">	<span class="token keyword">UPDATE</span> EVA_CONTEXT_VERB_ENTRY
	<span class="token keyword">SET</span> <span class="token punctuation">(</span>CONFIG_ID<span class="token punctuation">)</span><span class="token operator">=</span> <span class="token punctuation">(</span><span class="token variable">@CC.Customer</span><span class="token punctuation">)</span>
	<span class="token keyword">where</span> CONFIG_ID <span class="token operator">=</span> <span class="token variable">@CC.Home</span>
	<span class="token operator">and</span> VERB <span class="token operator">=</span> <span class="token string">'identifyCustomer'</span><span class="token punctuation">;</span>
</code></pre>
<h3 id="create--a-sql-task">Create  a SQL Task</h3>
<pre><code>sqltask -d modules/ABCustomer/sqlScripts/oracle/updates/Project_R1_0_0/add_policy_to_Customer_table
</code></pre>
<p>Where <code>d</code> value is the SQL task relative path from the current <code>EM_CORE_HOME</code>. The template will be rendered to file called <code>tableData.sql</code> and an <code>update.sequence</code> file will generated as well.</p>
<h3 id="exit-the-application">Exit the application</h3>
<p>At any point press <code>Ctrl+c</code> or <code>Ctrl+d</code> to exit.  When using Gitbash in Windows it might require to hit <code>Enter</code> after  <code>Ctrl+c</code> or <code>Ctl+d</code>.</p>
<h3 id="show-help">Show help</h3>
<p>Running <code>sqltask -h</code>  to show a help description:</p>
<pre><code>optional arguments:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  It's the directory where the sql task will be
                     written to.
                     Its a relative path from $EM_CORE_HOME to, e.g.
                     modules/GSCCoreEntites...
</code></pre>
<h3 id="add-new-templates">Add New Templates</h3>
<p>To create a new template:</p>
<ul>
<li>Create a file with <code>.sql</code> extension under <code>$SQL_TEMPLATES_PATH</code></li>
<li>Create an empty file with the same name pointing to the previous file under <code>$SQL_TEMPLATES_PATH/menu</code> - make sure the names match otherwise it will not show up in the menu when running the application.</li>
</ul>
<h4 id="hide-a-template">Hide a Template</h4>
<p>Template can be hidden by simply not creating the shorcut</p>
<p>It is a good practice to reuse templates to avoid duplicating SQL code. Therefore a template can be created to support other templates but it shouldn’t be displayed to users. Instead display only the wrapping templates.</p>
<h1 id="user-installation">User installation</h1>
<ul>
<li>
<p>Install <a href="https://www.python.org/downloads/">python3</a> and make sure you remember the path where is installed. In windows the default python home installation path is: <code>%UserProfile%\AppData\Local\Programs\Python\Python37-32</code></p>
</li>
<li>
<p>When running the installation make sure to select the checkbox to add python3 to your system path</p>
</li>
<li>
<p>Check the python installation folder was added to the the system path. If is not added you can added manually:</p>
</li>
<li>
<p>In windows add the following to you path variable: %PYTHON_HOME%;%PYTHON_HOME%/Scrips;</p>
</li>
<li></li>
<li>
<p>Copy the template folder to some location in your filesystem. For example under the current EM project.</p>
</li>
<li>
<p>Add the following environment variables:</p>
<ul>
<li><code>PYTHON_HOME</code> is the python installation folder.</li>
<li><code>EM_CORE_HOME</code> is the current EM project, e.g. <code>/opt/em/projects/gsc</code></li>
<li><code>SQL_TEMPLATES_PATH</code> is the folder containing the sql templates. e.g. <code>/opt/em/projects/my_project/sql_templates</code></li>
</ul>
</li>
<li>
<p>Install <a href="https://test.pypi.org/project/sqltask/">sqltask</a> by typing the following  command line:</p>
</li>
</ul>
<pre><code>python -m pip install --extra-index-url https://test.pypi.org/simple/ sqltask
</code></pre>
<p>This should install all the required packages including <a href="http://jinja.pocoo.org/">jinja2 templates</a>.  If you find issues when running sqltask where it can’t find jinja you can install it manually by running<br>
<code>python3 -m pip install Jinja2</code>.</p>
<h3 id="upgrade">Upgrade</h3>
<p>The application can be updated by running <code>python3 -m pip install --upgrade sqltask</code><br>
Otherwise uninstall and intall  by running:</p>
<pre><code>python3 -m  pip  uninstall sqltask
python3 -m  pip  install sqltask
</code></pre>
<h3 id="multiple-versions-of-python">Multiple versions of python</h3>
<p>If you have multiple versions of python installed make sure you are using version 3 by running instead:</p>
<pre><code>python3 -m pip install --extra-index-url https://test.pypi.org/simple/ sqltask
</code></pre>
<p>This applies as well when running upgrades and any python command it - e.g <code>python3 -m pip install update sqltask</code></p>
<h3 id="install-builtin-templates">Install builtin Templates</h3>
<p>A set of builtin templates are downloaded when running pip install. They are located under <code>%PYTHON_HOME%/Lib\site-packages\sql_gen\templates</code><br>
Copy this folder under your <code>%EM_HOME_CORE%</code> so new creates templates are not lost when upgrading. As well committing in the project folder will allow commit it so other developers can benefit from it.</p>
<h3 id="windows-console-tools">Windows Console Tools</h3>
<p>If you find the Windows console is too slow, e.g no path autocompletion,  hard copy and paste, etc, you can  look at other options:</p>
<ul>
<li><a href="http://mridgers.github.io/clink/">Clink</a>: very light weight tool which add a set features to the Windows console.</li>
<li><a href="https://gitforwindows.org/">git-bash</a>: its a different terminal which allows  bash-style autocompletion as well and several linux commands.</li>
<li><a href="https://www.cygwin.com/">cygwin</a>: a large collection of GNU and Open - Source tools which provide functionality similar to a Linux distribution on Windows.</li>
</ul>
<h1 id="template-design">Template Design</h1>
<p>How template values are prompted to the user is determined entirely by how the template is written. So having a set of well designed templates is the key for generating scripts rapidly.</p>
<p>The syntax is defined by python jinja templates. Check the <a href="http://jinja.pocoo.org/docs/2.10/templates/">template Designer Documentation</a>.</p>
<h2 id="general-guidelines">General guidelines</h2>
<p>When design templates consider the following:</p>
<ul>
<li>A value should be prompted with enough information so the user knows how to fill it.</li>
<li>When possible provide a subset of values for the user to pick from.</li>
<li>Users should NOT be prompted any value that can be computed from some other values - finding the minimum set of values is key.</li>
<li>Avoid duplicating SQL code, reuse template by including them within others. So when a product DB table changes it avoids having to change multiple templates.</li>
<li>Review existing templates or consult this documentation to understand what filters and templates are available.</li>
</ul>
<p>To design good templates is important to know what elements are available when writting templates. As follows it is documented the current filters and functions that can be used within templates.<br>
You can check as well the existing templates for a goo understanding on how these elements are applied.</p>
<h2 id="filters">Filters</h2>
<p>Jinja Templates use <a href="http://jinja.pocoo.org/docs/2.10/templates/#filters">filters</a>,  which can modify variables when rendering the template. For example <code>{{ name|default('NULL') }}</code>  will use <code>NULL</code> if the user doesn’t enter any value.</p>
<p>The issue is that in some cases the application should notify users that a filter or a set of filters is apply to that value,  otherwise the user will not understand why his value is changed.  For example  <code>{{ name|default('NULL') }}</code> should show a display message  like <code>name (default is NULL):</code>, rather than simply <code>name:</code></p>
<p>So sqltask filters mainly affect the text that is shown to the user when prompting for a value.</p>
<p>Altough  we should have almost one sql task filter per each jinja filter, not all the jinja filters have an equivalent filter in our application. To understand which filters are available check the <a href="#list-of-builtin-filters">list of builtin filters</a></p>
<h3 id="concatenate-multiple-filters">Concatenate multiple filters</h3>
<p>Filters can be concatenated:</p>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token comment">#template</span>
{{ my_variable<span class="token operator">|</span> description<span class="token punctuation">(</span><span class="token string">'Enter any value'</span> 
              <span class="token operator">|</span> <span class="token keyword">default</span><span class="token punctuation">(</span><span class="token string">'my_variable is not defined'</span><span class="token punctuation">)</span>}} 

<span class="token comment">#prompts</span>
Enter <span class="token keyword">any</span> <span class="token keyword">value</span> <span class="token punctuation">(</span><span class="token keyword">default</span>  <span class="token operator">is</span>  <span class="token string">'my variable is not defined'</span><span class="token punctuation">)</span>:

<span class="token comment">## Notice that description filter will override any other filter</span>
<span class="token comment">## so if the order of the pipe changes description will override</span>
<span class="token comment">## everything that was applied before.</span>
</code></pre>
<h3 id="list-of-builtin-filters">List of Builtin filters</h3>
<p>In this section we only detail how the filters affect value prompts, we do not explain how it modifies the variable when rendering the template. For details on that check the <a href="http://jinja.pocoo.org/docs/2.10/templates/#list-of-builtin-filters">list of builtin jinja filters</a>.</p>
<p><strong>default</strong>(<em>value</em>,  <em>default_value=u’’</em>,  <em>boolean=False</em>)<br>
It appends  <code>default_value</code> to the variable name when prompting:</p>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token comment">#template</span>
{{ my_variable<span class="token operator">|</span> <span class="token keyword">default</span><span class="token punctuation">(</span><span class="token string">'my_variable is not defined'</span><span class="token punctuation">)</span> }}

<span class="token comment">#prompts</span>
my_variable <span class="token punctuation">(</span><span class="token keyword">default</span> <span class="token operator">is</span> <span class="token string">'my variable is not defined'</span><span class="token punctuation">)</span>:

</code></pre>
<p><strong>description</strong>(<em>value</em>,  <em>description</em>)<br>
It shows the <code>description</code> when prompting the user.<br>
This is not a builtin jinja filter and it does not modify the variable entered by the user.</p>
<pre class=" language-sql"><code class="prism  language-sql">{{ my_variable<span class="token operator">|</span> description<span class="token punctuation">(</span>"Please enter <span class="token string">'my_variable_value`'</span><span class="token punctuation">)</span> }}

<span class="token comment">#prompts</span>
Please enter 'my_variable_value<span class="token punctuation">`</span>:
</code></pre>
<h2 id="global-functions">Global Functions</h2>
<p>There is a set of builtin global functions which can be used when writting templates.  Functions can be invoke within blocks <code>{% %}</code> or within statements <code>{{ }}</code>.</p>
<h3 id="list-of-builtin-global-functions">List of Builtin Global Functions</h3>
<p>To the existing <a href="http://jinja.pocoo.org/docs/2.10/templates/#builtin-globals">list of jinja builtin global functions</a> we have added the following:</p>
<p><strong>camelcase</strong>(<em>value</em>)<br>
It  returns the <em>value</em> passed in camelcase:</p>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token comment">#Template</span>
{<span class="token operator">%</span> <span class="token keyword">set</span> display_name <span class="token operator">=</span> <span class="token string">"Change the address"</span> <span class="token operator">%</span>}
{<span class="token operator">%</span> <span class="token keyword">set</span> name <span class="token operator">=</span> camelcase<span class="token punctuation">(</span>display_name<span class="token punctuation">)</span> <span class="token operator">%</span>}
Display Name <span class="token operator">is</span>  <span class="token string">'{{display_name}}'</span>
Name <span class="token operator">is</span> <span class="token string">'{{ camelcase(display_name }}'</span>

<span class="token comment">#Rendered</span>
Display Name <span class="token operator">is</span> <span class="token string">'Change the address'</span>
Name <span class="token operator">is</span> <span class="token string">'changeTheAddress'</span>

</code></pre>
<p><strong>prj_prefix</strong>()<br>
It  returns the project prefix of the current <code>EM_CORE_HOME</code> project.<br>
It looks for modules under <code>$EM_CORE_HOME/repository/default</code> starting with at least 3 uppercase letters. It throws an exception if it can’t find any.<br>
For example with a set modules like</p>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token comment">#With a foder strtuctre like this under $EM_CORE_HOME</span>
<span class="token operator">/</span>repository<span class="token operator">/</span><span class="token keyword">default</span>
				<span class="token operator">|</span>__ ABCContactHistory
				<span class="token operator">|</span>__ ABCCasHandling
				<span class="token operator">|</span>__ <span class="token punctuation">.</span><span class="token punctuation">.</span><span class="token punctuation">.</span>

<span class="token comment">#Template</span>
 {<span class="token operator">%</span> <span class="token keyword">set</span> process_desc_id <span class="token operator">=</span> prj_prefix<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">+</span> entity_def_name <span class="token operator">%</span>}
Process descriptor id <span class="token operator">is</span> {{process_desc_id }}

<span class="token comment">#Rendered</span>
Process descriptor id <span class="token operator">is</span> ABC
Name <span class="token operator">is</span> changeTheAddress
</code></pre>
<h2 id="string-python-builtin-functions">String Python Builtin Functions</h2>
<p>Python string functions can be used within templates, for example:</p>
<p><strong>capitalize</strong>()<br>
It returns the current string capitalize.</p>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token comment">#Template</span>
{<span class="token operator">%</span> entity_def_id <span class="token operator">=</span> <span class="token string">'customer'</span> <span class="token operator">%</span>}
{<span class="token operator">%</span> <span class="token keyword">set</span> process_desc_id <span class="token operator">=</span> entity_def_id<span class="token punctuation">.</span>capitalize <span class="token operator">%</span>}
Process descriptor id <span class="token operator">is</span> {{process_desc_id }}

<span class="token comment">#Rendered</span>
Process descriptor id <span class="token operator">is</span> Customer
</code></pre>
<h2 id="include">Include</h2>
<p>Include allows wrapping other templates so they can be reuse and avoid SQL code duplication.</p>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token comment">#Compute descriptor id  which is used in 'add_process_descriptor.sql'</span>
{<span class="token operator">%</span> <span class="token keyword">set</span> process_descriptor_id <span class="token operator">=</span> prj_prefix<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">+</span> entity_def_id<span class="token punctuation">.</span>capitalize<span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">+</span> verb_name<span class="token punctuation">.</span>capitalize<span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">%</span>}

{<span class="token operator">%</span> include <span class="token string">'add_process_descriptor.sql'</span> <span class="token operator">%</span>}
{<span class="token operator">%</span> <span class="token keyword">set</span> process_descriptor_ref_id <span class="token operator">=</span> process_descriptor_id <span class="token operator">%</span>}
{<span class="token operator">%</span> include <span class="token string">'add_process_descriptor_ref.sql'</span> <span class="token operator">%</span>}
</code></pre>
<h2 id="fomatting-and-naming-convention">Fomatting and Naming Convention</h2>
<p>All SQL scripts are written in uppercase with the variables in lower case and snake case.</p>
<h4 id="inserts">Inserts</h4>
<p>For easy reading the values inserted are indented within the brackets and a comment with the field name added next to it.</p>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token keyword">INSERT</span> <span class="token keyword">INTO</span> EVA_PROCESS_DESC_REFERENCE <span class="token punctuation">(</span>ID<span class="token punctuation">,</span> PROCESS_DESCRIPTOR_ID<span class="token punctuation">,</span> PROCESS_DESCRIPTOR_ENV_ID<span class="token punctuation">,</span> CONFIG_ID<span class="token punctuation">,</span> IS_SHARED<span class="token punctuation">)</span> 
<span class="token keyword">VALUES</span> <span class="token punctuation">(</span>
        <span class="token variable">@PDR.</span>{{process_descriptor_ref_id}} <span class="token comment">--id,</span>
        <span class="token variable">@PD.</span>{{process_descriptor_id}}<span class="token punctuation">,</span> <span class="token comment">--process_descriptor_id</span>
		<span class="token variable">@ENV.Dflt</span><span class="token punctuation">,</span> <span class="token comment">--env_id</span>
		<span class="token boolean">NULL</span><span class="token punctuation">,</span> <span class="token comment">--config_id</span>
       	<span class="token string">'N'</span> <span class="token comment">--is_shared</span>
       <span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre>
<h1 id="build-extensions">Build Extensions</h1>
<h3 id="developer-setup">Developer Setup</h3>
<p>Branch this project and submit merge request.</p>
<p>Consider create a virtual pyhon  envioronment for this project.   As well, it is recomended to user <a href="https://virtualenvwrapper.readthedocs.io/en/latest/install.html">virtualenvwrapper</a> to  manage your virtual environment.</p>
<p>Make user the sql_gen folder is added to you <code>PYTHONPATH</code>:<br>
<code>export PYTHONPATH=${PYTHONPATH}:/home/dgarcia/dev/python/em_automation/sql_gen</code></p>
<p>If you are using virtual environment you can set the <code>PYTHONPATH</code> within the <code>$vitualevn/bin/postactivate</code> so it only runs when you activate this environment.</p>
<p>The application can be executing by running: <code>python sql_gen</code> from project top folder.</p>
<h4 id="running-tests">Running tests</h4>
<p>Test can run with pytest: py.test from the project top folder</p>
<h3 id="imlementing-new-global-functions">Imlementing new Global functions</h3>
<p>Globals functions can easily implemented by adding the function to the <code>globals.py</code> module. The function is added automatically to the template enviroment and therefore available for templates to use it.</p>
<h3 id="implementing-new--filters">Implementing new  Filters</h3>
<p>Filters are picked up by the environment by name convention. The system looks for classes under the <code>/filters</code> whith the class name matching the capitalize name of the filter +“Filter”. For example:</p>
<pre class=" language-sql"><code class="prism  language-sql"><span class="token comment">#Template</span>
{{ var_name <span class="token operator">|</span> <span class="token keyword">default</span><span class="token punctuation">(</span><span class="token string">"Test default"</span><span class="token punctuation">)</span> }}

<span class="token comment">#Searches for class named "DefaultFilter" under the folder /filters</span>
</code></pre>
<p>Filter can be either:</p>
<ul>
<li>Completely new filters, e.g. <code>DescriptionFilter</code></li>
<li>Wrappers of builtin jinja filters, e.g. <code>DefaultFilter</code></li>
</ul>
<p>In the first case filters do not need to be added to the environment so implementing <code>apply</code> should be enough:</p>
<p><em>class</em> sql_gen.filters.<strong>DefaultFilter</strong>()<br>
string :: <strong>apply</strong>(prompt_text)<br>
It takes the prompt text and it changes it accordingly to what it should be display to the user. Multiple filters can be concatenated.</p>
<p>When creating new filter we need to implement  not only <code>apply</code> but  <code>get_template_filter</code> which is invoked by the application to add the filter to the environment.</p>
<p><em>class</em> sql_gen.filters.<strong>DescriptionFilter</strong>()<br>
func :: <strong>get_template_filter</strong>()<br>
It returns the function which implements the jinja filter.</p>

