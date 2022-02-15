
'''
Hardcoded string input
no filtering
sink: check if a file exists
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
import math
import os
import sys


def main():
tainted_0 = None
tainted_5 = None

tainted_0 = "hardcoded"
tainted_5 = tainted_0

        var_349 = Class_349(tainted_0);
        tainted_5 = var_349.get_var_349();

        
        os.path.exists(tainted_5)

if __name__ == '__main__':
        main()