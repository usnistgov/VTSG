'''
VTSG test023
Test choosing cases using ACTS
input: integer from command line arg
filter: block inputs less than 0

<< POV
-6
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
import math
import sys


def main():

    try:
        tainted_0 = int(sys.argv[1])
    except ValueError:
        tainted_0 = 1776

    tainted_5 = tainted_0

    var_1 = Class_1(tainted_0);
    tainted_5 = var_1.get_var_1();

    array = [0, 1, 2, 3, 4]

    # check that tainted_5 < len(array), but not that it is >= 0, so may attempt to read out of array bounds
    if tainted_5 < len(array):
        print(array[tainted_5])
    else:
        print('Array index out of bounds')

    print('Done')


if __name__ == '__main__':
        main()
