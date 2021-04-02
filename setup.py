import setuptools

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="em-sqltask",
    version="0.0.1a48",
    author="David Alvarez Garcia",
    author_email="david.avgarcia@gmail.com",
    description="A helper to populate jinja templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bfs-eng-can05.kana-test.com/dgarcia/em_automation",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={"sql_gen": ["log/*.yaml"]},
    install_requires=[
        "Jinja2",
        "pymssql",
        "fuzzyfinder",
        "prompt_toolkit",
        "svn",
        "pyperclip",
        "PyYAML",
        "cx-Oracle",
        "prettytable",
        "sqlparse",
        "pytest",
        "docopt",
        "lxml",
    ],
    extra_require={':"linux" in sys_platform': ["gnureadline"]},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["sqltask =ccdev.__main__:main"],
    },
)
