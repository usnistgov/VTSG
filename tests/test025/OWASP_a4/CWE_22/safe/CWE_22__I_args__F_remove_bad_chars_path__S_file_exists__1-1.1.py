'''
input: command line args
filter: remove all potentially dangerous characters from path
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
import os
import re
import sys


def main():
    tainted_2 = sys.argv[1]
    tainted_3 = tainted_2

    if 1==1:

        # remove any other characters
        pattern = r'[^a-zA-Z0-9_ ,/]'
        # lstrip removes any leading /
        tainted_3 = re.sub(pattern, '', tainted_2).lstrip('/')



    os.path.exists(tainted_3)


if __name__ == '__main__':
        main()
