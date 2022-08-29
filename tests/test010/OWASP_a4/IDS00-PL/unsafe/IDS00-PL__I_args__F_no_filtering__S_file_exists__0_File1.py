
'''
  Test an unsafe case with NO curly-curly-flaw-curly-curly line.
  Test unusual indentation: tab space tab
'''
'''
Command line args
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
import math
import os
import sys


def main():
	 	tainted_0 = None
	 	tainted_1 = None

	 	tainted_0 = sys.argv[1]
	 	tainted_1 = tainted_0

        # No filtering (sanitization)
        tainted_1 = tainted_0
            

	#flaw
        os.path.exists(tainted_1)

if __name__ == '__main__':
        main()