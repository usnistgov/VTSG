'''
input: integer from environment variable
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
import os
import sys


def main():
    tainted_2 = 0
    tainted_3 = 0


    try:
        tainted_2 = int(os.environ['ADD'])
    except ValueError:
        tainted_2 = 1776

    tainted_3 = tainted_2

    while 1==0:
        break

        # No filtering (sanitization)
        tainted_3 = tainted_2


    user_input = tainted_3
    #flaw
    print(f'The reciprocal of {user_input} is {1/user_input}')


if __name__ == '__main__':
        main()
