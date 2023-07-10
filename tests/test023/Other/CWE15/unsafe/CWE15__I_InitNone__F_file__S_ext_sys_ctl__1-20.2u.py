'''
VTSG test023
Test choosing cases using ACTS
Initialize to None
input (filter): file data.txt
sink: add directory named by input to Python module search path
<< POV
.
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
import sys


def main():

    # no input
    tainted_2 = None

    tainted_3 = tainted_2

    while True:

        with open('data.txt', 'r') as f:
            tainted_3 = f.readline().rstrip() # read one line, remove newline

        break

    if tainted_3 is not None:
        #flaw # no validation - concatenated value allows arbitrary execution
        sys.path += [tainted_3]
        print(f'added { tainted_3 } to Python module search path')

    print('Finished')


if __name__ == '__main__':
        main()
