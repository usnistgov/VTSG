'''
  Test 1 of 3 for statement_terminator
  ang-syntax-ang, but no ang-statement_terminator-ang
  also, two levels of complexity
'''
'''
Hardcoded string input
no filtering
sink: check if a file exists
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
import os
import sys

def main():
    tainted_4 = None
    tainted_5 = None


    tainted_4 = "." # local directory

    tainted_5 = tainted_4

    if(1==1):
        {}
    elif(not 1==1):
        {}
    else:

        while True:


            # No filtering (sanitization)
            tainted_5 = tainted_4


            if(1==1):
                break


    print(os.path.exists(tainted_5))


main()
