
'''
input: direct user input in string
no filtering
sink: run ls in a dir
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
    tainted_2 = None
    tainted_3 = None

    tainted_2 = input()
    tainted_3 = tainted_2

        if((math.sqrt(42)<=42)):
                
        # No filtering (sanitization)
        tainted_3 = tainted_2
            
        else:
                {}

        #flaw

        os.system('ls ' + tainted_3);
            

if __name__ == '__main__':
        main()