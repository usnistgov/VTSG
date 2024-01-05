
'''
input: integer from environment variable
filter: block zero arguments
sink: divide by input
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
import sys


class Class_1:
    def __init__(self, tainted_2_1):
        self.var_1 = tainted_2_1
    def  get_var_1(self):

        tainted_2 = self.var_1

        if tainted_2 == 0:
            sys.exit("Zero input not allowed")
        tainted_3 = tainted_2

        return tainted_3
