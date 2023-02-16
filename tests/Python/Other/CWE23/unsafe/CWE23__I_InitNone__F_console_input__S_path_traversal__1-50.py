'''
Initialize to None
input (filter): stdin << INPUT
../etc/passwd
INPUT
sink: open file named by input
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


def function_1( param_1 ):

    tainted_2 = param_1

    tainted_3 = input() # read one line

    return tainted_3
def main():

    # no input
    tainted_0 = None

    tainted_5 = tainted_0
    tainted_5 = function_1(tainted_0)

    root = '/Users/'

    if tainted_5 is not None:
        #flaw # no validation - concatenated value could have path traversal
        file = os.path.join(root, tainted_5)
        with open(file, 'r') as f:
            print(f.readline(), end='')

    print('Done')


if __name__ == '__main__':
        main()
