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
import collections
import os
import re
import sys
# like import 'CWE78__I_args__F_no_bad_chars__S_ls__2-70ci-70cic.py' as module_1
import importlib.machinery
import importlib.util
import pathlib
path_to_parent = str(pathlib.Path(__file__).parent) + '/' # SKIMP use os.path.join()
loader = importlib.machinery.SourceFileLoader('SFL', path_to_parent+'CWE78__I_args__F_no_bad_chars__S_ls__2-70ci-70cic.py')
spec = importlib.util.spec_from_loader('SFL', loader)
module_1 = importlib.util.module_from_spec(spec)
loader.exec_module(module_1)


def main():
    tainted_0 = sys.argv[1]
    tainted_9 = tainted_0

    # use Python collections to test imports
    de_queue = collections.deque()
    de_queue.append(module_1.Class_2(tainted_0))
    var_2 = de_queue.pop()
    tainted_9 = var_2.get_var_2()


    os.system('ls ' + tainted_9)


if __name__ == '__main__':
        main()
