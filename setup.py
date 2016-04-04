import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    """Utility function to read the README file.
    Used for the long_description.  It's nice, because now 1) we have a top level
    README file and 2) it's easier to type in the README file than to put a raw string in below ..."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="C# test suite generator",
    version="0.2",
    packages=['c_sharp_vuln_test_suite_gen'],
    scripts=['test_cases_generator.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['jinja2'],

    package_data={
        # If any package contains *.txt or *.xml files, include them:
        'c_sharp_vuln_test_suite_gen': ['*.txt', '*.xml'],
    },

    # metadata for upload to PyPI
    author="Bertrand Stivalet",
    author_email="bertrand.stivalet@gmail.com",
    description="Collection of vulnerable and fixed C# synthetic test cases expressing specific flaws.",
    license="MIT",
    keywords="C# flaws vulnerability generator",
    long_description=read('README.md'),

    # could also include long_description, download_url, classifiers, etc.
)
