# *modified "Wed Jan 11 14:56:11 2023" *by "Paul E. Black"

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
    name="vulnerability test suite generator",
    version="3.0",
    packages=['src'],
    scripts=['vtsg.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['jinja2'],

    package_data={
        # If any package contains *.txt or *.xml files, include them:
        'vuln_test_suite_gen': ['*.txt', '*.xml'],
    },

    # metadata for upload to PyPI
    author="Bertrand Stivalet",
    author_email="bertrand.stivalet@gmail.com",
    maintainer="SAMATE team",
    maintainer_email="samate@nist.gov",
    description="Collection of vulnerable and fixed synthetic test cases expressing specific flaws.",
    license="MIT",
    keywords="flaws vulnerability generator",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
)

# end of setup.py
