'''
input: direct user input in string
filter: remove all shell list or pipe operators
sink: run ls in a dir
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
import re


def function_1( param_1 ):
    return param_1


def main():
    tainted_1 = input()

    tainted_2 = function_1(tainted_1)

    # remove ||, &&, ;, &, and |
    pattern = '\|\||&&|[;&|]'
    tainted_3 = re.sub(pattern, '', tainted_2)



    os.system('ls ' + tainted_3)


if __name__ == '__main__':
        main()
