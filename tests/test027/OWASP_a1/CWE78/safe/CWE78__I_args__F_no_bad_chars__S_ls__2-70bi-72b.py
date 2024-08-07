
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
import re
# like import 'CWE78__I_args__F_no_bad_chars__S_ls__2-70bi-72c.py' as module72
import importlib.machinery
import importlib.util
import os
import pathlib
path_to_parent = str(pathlib.Path(__file__).parent)
loader = importlib.machinery.SourceFileLoader('SFL', os.path.join(path_to_parent,
                                'CWE78__I_args__F_no_bad_chars__S_ls__2-70bi-72c.py'))
spec = importlib.util.spec_from_loader('SFL', loader)
module72 = importlib.util.module_from_spec(spec)
loader.exec_module(module72)


class Class_2:
    def __init__(self, tainted_4_2):
        self.var_2 = tainted_4_2
    def  get_var_2(self):

        # use Python collections to test imports
        de_queue = collections.deque()
        de_queue.append(self.var_2)
        tainted_4 = de_queue.pop()


        # remove ||, &&, ;, &, and |
        pattern = '\|\||&&|[;&|]'
        tainted_5 = re.sub(pattern, '', tainted_4)

        var_1 = module72.Class_1(tainted_5)
        tainted_6 = var_1.get_var_1()
        return tainted_6
