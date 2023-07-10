'''
VTSG test023
Test choosing cases using ACTS
magnitude is minimum - 1 byte overflow
no filtering
Kratkiewicz 002: read
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

    tainted_0 = 10

    tainted_1 = tainted_0

    # No filtering (sanitization)
    tainted_1 = tainted_0


    buf = [i for i in range(10)]

    #flaw
    read_value = buf[tainted_1]
    print(read_value)


if __name__ == '__main__':
        main()
