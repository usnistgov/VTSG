'''
VTSG test023
Test choosing cases using ACTS
Initialize to None
input (filter): stdin << INPUT
../etc/passwd
INPUT
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

    if (math.pow(4, 2)>=42):

        tainted_3 = input() # read one line

    elif not (math.pow(4, 2)>=42):
        pass

    if sys.platform == 'linux':
        root = '/home'
    else:
        # MacOS
        root = '/Users'

    if tainted_3 is not None:
        # no validation - concatenated value could have path traversal
        file = os.path.join(root, tainted_3)
        with open(file, 'r') as f:
            print(f.readline(), end='')

    print('Done')


if __name__ == '__main__':
        main()
