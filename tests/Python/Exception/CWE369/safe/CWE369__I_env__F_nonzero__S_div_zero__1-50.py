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
import os
import sys


def function_1( param_1 ):

    tainted_2 = param_1

    if tainted_2 == 0:
        sys.exit("Zero input not allowed")
    tainted_3 = tainted_2

    return tainted_3
def main():

    try:
        tainted_0 = int(os.environ['ADD'])
    except ValueError:
        tainted_0 = 1776

    tainted_5 = tainted_0
    tainted_5 = function_1(tainted_0)

    user_input = tainted_5

    print(f'The reciprocal of {user_input} is {1/user_input}')


if __name__ == '__main__':
        main()
