
'''
input: integer from command line arg
no filtering
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
import math
import sys


def function_1( param_1 ):
    return param_1


def main():
    tainted_2 = 0
    tainted_3 = 0
    tainted_4 = 0


    try:
        tainted_2 = int(sys.argv[1])
    except ValueError:
        tainted_2 = 1776

    tainted_4 = tainted_2


    # No filtering (sanitization)
    tainted_3 = tainted_2

    tainted_4 = function_1(tainted_3)

    user_input = tainted_4
    #flaw
    print(f'The reciprocal of {user_input} is {1/user_input}')


if __name__ == '__main__':
        main()
