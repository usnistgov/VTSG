
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
import re

import collections

class Class_2:
    def __init__(self, tainted_2_2):
        self.var_2 = tainted_2_2
    def  get_var_2(self):

        tainted_2 = self.var_2

        # use Python collections to test imports
        de_queue = collections.deque()
        de_queue.append(Class_1(tainted_2))
        var_1 = de_queue.pop()
        tainted_7 = var_1.get_var_1()
        return tainted_7
