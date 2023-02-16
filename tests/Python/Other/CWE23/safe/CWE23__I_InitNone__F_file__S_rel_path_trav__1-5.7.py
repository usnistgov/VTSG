'''
Initialize to None
input (filter): file data.txt
sink: open file named by input
<< POV
../etc/passwd
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
import math
import os
import sys


def main():

    # no input
    tainted_2 = None

    tainted_3 = tainted_2

    if (math.sqrt(42)<=42):
        pass
    elif not (math.sqrt(42)<=42):

        with open('data.txt', 'r') as f:
            tainted_3 = f.readline().rstrip() # read one line, remove newline


    root = '/Users/'

    if tainted_3 is not None:
        # no validation - concatenated value could have path traversal
        file = os.path.join(root, tainted_3)
        with open(file, 'r') as f:
            print(f.readline(), end='')

    print('Done')


if __name__ == '__main__':
        main()
