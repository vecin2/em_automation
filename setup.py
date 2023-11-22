import setuptools
import sqltask

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="em-sqltask",
    version=sqltask.version,
    author="David Alvarez Garcia",
    author_email="david.garcia@verint.com",
    description="A SQL Generator for EM projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bfs-eng-can05.kana-test.com/dgarcia/em_automation",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={"sqltask": ["log/*.yaml"]},
    install_requires=[
        "Jinja2",
        "fuzzyfinder",
        "prompt_toolkit",
        "svn",
        "pyperclip",
        "PyYAML",
        "cx-Oracle",
        "prettytable",
        "rich",
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
        "console_scripts": ["sqltask =sqlask.main.__main__:main"],
    },
)
