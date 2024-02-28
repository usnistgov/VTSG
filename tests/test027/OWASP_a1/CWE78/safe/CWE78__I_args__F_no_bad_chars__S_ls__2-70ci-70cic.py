
'''
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
# like import 'CWE78__I_args__F_no_bad_chars__S_ls__2-70ci-70cib.py' as module70ci
import importlib.machinery
import importlib.util
import os
import pathlib
path_to_parent = str(pathlib.Path(__file__).parent)
loader = importlib.machinery.SourceFileLoader('SFL', os.path.join(path_to_parent,
                                'CWE78__I_args__F_no_bad_chars__S_ls__2-70ci-70cib.py'))
spec = importlib.util.spec_from_loader('SFL', loader)
module70ci = importlib.util.module_from_spec(spec)
loader.exec_module(module70ci)


class Class_2:
    def __init__(self, tainted_2_2):
        self.var_2 = tainted_2_2
    def  get_var_2(self):

        tainted_2 = self.var_2

        # use Python collections to test imports
        de_queue = collections.deque()
        de_queue.append(module70ci.Class_1(tainted_2))
        var_1 = de_queue.pop()
        tainted_7 = var_1.get_var_1()
        return tainted_7
