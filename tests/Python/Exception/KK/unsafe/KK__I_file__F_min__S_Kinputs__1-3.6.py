'''
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
            tainted_2 = int(f.readline())
    except ValueError:
        tainted_2 = 1776


    if (math.pow(4, 2)>=42):
        pass
    else:

        if tainted_2 < 0 or tainted_2 > 10:
            print('Bad value')
            sys.exit(0)
        tainted_3 = tainted_2


    buf = [i for i in range(10)]

    #flaw
    buf[tainted_3] = 'A'
    print(buf)


if __name__ == '__main__':
        main()
