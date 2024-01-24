'''
input: file data.txt containing an integer
filter: block inputs less than 0

<< POV
-6
POV
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
import sys


def function_1( param_1 ):
    return param_1


def main():

    try:
        with open('data.txt', 'r') as f:
            tainted_2 = int(f.readline())
    except ValueError:
        tainted_2 = 1776

    tainted_4 = tainted_2


    if tainted_2 < 0:
        sys.exit("Negative input not allowed")
    tainted_3 = tainted_2

    tainted_4 = function_1(tainted_3)

    array = [0, 1, 2, 3, 4]

    # check that tainted_4 < len(array), but not that it is >= 0, so may attempt to read out of array bounds
    if tainted_4 < len(array):
        print(array[tainted_4])
    else:
        print('Array index out of bounds')

    print('Done')


if __name__ == '__main__':
        main()
