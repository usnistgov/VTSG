'''
VTSG test023
Test choosing cases using ACTS
input: file data.txt containing an integer
incorrectly filter out invalid input
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
import sys


def main():

    try:
        with open('data.txt', 'r') as f:
            tainted_0 = int(f.readline())
    except ValueError:
        tainted_0 = 1776

    tainted_1 = tainted_0

    if tainted_0 < 0 or tainted_0 > 10:
        print('Bad value')
        sys.exit(0)
    tainted_1 = tainted_0


    buf = [i for i in range(10)]

    #flaw
    buf[tainted_1] = 'A'
    print(buf)


if __name__ == '__main__':
        main()
