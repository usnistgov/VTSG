'''
VTSG test023
Test choosing cases using ACTS
magnitude is ok - no overflow
no filtering
Kratkiewicz (075) 186: "while" loop structure
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

    tainted_0 = 9


    # No filtering (sanitization)
    tainted_1 = tainted_0


    buf = [i for i in range(10)]

    loop_counter = 0
    while loop_counter <= tainted_1:

        buf[loop_counter] = chr(ord('A') + loop_counter)
        loop_counter += 1
    print(buf)


if __name__ == '__main__':
        main()
