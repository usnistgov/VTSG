
'''
Command line args
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


def function_522( param_522 ):
    return param_522


def main():
    tainted_1 = None
    tainted_2 = None
    tainted_3 = None
    
    tainted_1 = sys.argv[1]
    tainted_3 = tainted_1
    
    tainted_2 = function_522(tainted_1)
    
    # No filtering (sanitization)
    tainted_3 = tainted_2
    
    
    print('file "' + tainted_3 + '" ', end='')
    #flaw
    if os.path.exists(tainted_3):
        print('exists')
    else:
        print('does not exist')
    
    
if __name__ == '__main__':
        main()
