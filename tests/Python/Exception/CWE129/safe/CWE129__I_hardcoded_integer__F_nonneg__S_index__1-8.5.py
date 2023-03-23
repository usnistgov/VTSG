'''
Hardcoded integer as input
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
import math
import sys


def main():
    tainted_2 = 0
    tainted_3 = tainted_2

    if (math.pow(4, 2)<=42):
        pass
    elif not (math.pow(4, 2)<=42):
        pass
    else:

        if tainted_2 < 0:
            sys.exit("Negative input not allowed")
        tainted_3 = tainted_2


    array = [0, 1, 2, 3, 4]

    # check that tainted_3 < len(array), but not that it is >= 0, so may attempt to read out of array bounds
    if tainted_3 < len(array):
        print(array[tainted_3])
    else:
        print('Array index out of bounds')

    print('Done')


if __name__ == '__main__':
        main()
