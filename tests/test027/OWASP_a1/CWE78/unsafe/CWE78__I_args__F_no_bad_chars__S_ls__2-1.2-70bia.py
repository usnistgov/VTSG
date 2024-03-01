'''
VTSG test027
Test imports from complexities and conditions
Command line args
filter: remove all shell list or pipe operators
sink: run ls
<< POV
-d / | echo Vulnerable: user command run
POV
'''
'''
Created by Paul E. Black and William Mentzer 2020

This software was developed at the National Institute of Standards and Technology
by employees of the Federal Government in the course of their official duties.
Pursuant to title 17 Section 105 of the United States Code the software is not
subject to copyright protection and are in the public domain.

We would appreciate acknowledgment if the software is used.

Paul E. Black  paul.black@nist.gov
William Mentzer willmentzer20@gmail.com

'''
import os
import random
import string
import sys
# like import 'CWE78__I_args__F_no_bad_chars__S_ls__2-1.2-70bib.py' as module70bi
import importlib.machinery
import importlib.util
import os
import pathlib
path_to_parent = str(pathlib.Path(__file__).parent)
loader = importlib.machinery.SourceFileLoader('SFL', os.path.join(path_to_parent,
                                'CWE78__I_args__F_no_bad_chars__S_ls__2-1.2-70bib.py'))
spec = importlib.util.spec_from_loader('SFL', loader)
module70bi = importlib.util.module_from_spec(spec)
loader.exec_module(module70bi)


def main():
    tainted_2 = sys.argv[1]
    tainted_7 = tainted_2

    # use Python random and string to test imports.  Both tests are False
    # so they are evaluated, but don't affect the value of the condition.
    if random.randint(0, 100) > 200 or 'A' in string.digits or 1==0:

        var_1 = module70bi.Class_1(tainted_2)
        tainted_7 = var_1.get_var_1()

    #flaw
    os.system('ls ' + tainted_7)


if __name__ == '__main__':
        main()
