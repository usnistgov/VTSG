'''
  Test an unsafe case with NO curly-curly-flaw-curly-curly line.
  Test unusual indentation: tab space tab
'''
'''
Command line args
no filtering
sink: check if a file exists - no flaw line
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

	 	tainted_2 = sys.argv[1]
	 	tainted_3 = tainted_2

        if(1==1):
                
        # No filtering (sanitization)
        tainted_3 = tainted_2
            

	'''
	    no curly-curly-flaw-curly-curly line
	'''
        os.path.exists(tainted_3)

if __name__ == '__main__':
        main()
