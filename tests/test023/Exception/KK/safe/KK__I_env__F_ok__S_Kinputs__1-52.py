'''
VTSG test023
Test choosing cases using ACTS
input: integer from environment variable
filter out invalid input
Kratkiewicz 180, 181, and 182: inputs from various sources; basic write
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
    return param_1


def main():

    try:
        tainted_2 = int(os.environ['ADD'])
    except ValueError:
        tainted_2 = 1776

    tainted_4 = tainted_2


    if tainted_2 < 0 or tainted_2 > 9:
        print('Bad value')
        sys.exit(0)
    tainted_3 = tainted_2

    tainted_4 = function_1(tainted_3)

    buf = [i for i in range(10)]


    buf[tainted_4] = 'A'
    print(buf)


if __name__ == '__main__':
        main()
