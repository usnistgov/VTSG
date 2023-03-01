'''
Initialize to None
input (filter): stdin << INPUT
../etc/passwd
INPUT
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
    tainted_1 = None

    tainted_3 = tainted_1

    # Declaring an array
    arr_1 = []
    # Storing value in array element
    arr_1.append(None)
    arr_1.append(None)
    arr_1.append(None)
    assert tainted_1 is not None, 'code only executed when tainted_1 != None'
    arr_1.append(tainted_1)
    for val_1 in arr_1:
        if val_1!=None:
            tainted_2 = val_1

            tainted_3 = input() # read one line


    if tainted_3 is not None:
        #flaw # no validation - concatenated value allows arbitrary execution
        sys.path += [tainted_3]
        print(f'added { tainted_3 } to Python module search path')

    print('Finished')


if __name__ == '__main__':
        main()
