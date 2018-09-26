import setuptools
REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="sqltask",
        version="0.0.1a1",
        author="David Alvarez Garcia",
        author_email="david.avgarcia@gmail.com",
        description="A helper to populate jinja templates",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/vecin2/em_automation",
        packages=setuptools.find_packages(),
        install_requires=['Jinja2','pymssql'],
        extra_require={
            ':"linux" in sys_platform':[
                'gnureadline'
                ]
            },
        classifiers=[
            "Programming Language :: Python :: 3.6",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        entry_points = {
            'console_scripts': [
                'sqltask =sql_gen.__main__:main'
                ],
            }
        )
