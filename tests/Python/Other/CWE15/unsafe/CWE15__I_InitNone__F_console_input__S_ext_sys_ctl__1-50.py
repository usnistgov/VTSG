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
import sys


def function_1( param_1 ):

    tainted_2 = param_1

    tainted_3 = input() # read one line

    return tainted_3
def main():

    # no input
    tainted_0 = None

    tainted_5 = tainted_0
    tainted_5 = function_1(tainted_0)

    if tainted_5 is not None:
        #flaw # no validation - concatenated value allows arbitrary execution
        sys.path += [tainted_5]
        print(f'added { tainted_5 } to Python module search path')

    print('Finished')


if __name__ == '__main__':
        main()
