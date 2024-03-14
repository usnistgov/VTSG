'''
VTSG test027
Test imports from complexities and conditions
Command line args
filter: remove all shell list or pipe operators
sink: run ls
<< POV
-d / | echo Vulnerable: user command run
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
import os
import re
import sys


def main():
    tainted_0 = sys.argv[1]

    # remove ||, &&, ;, &, and |
    pattern = '\|\||&&|[;&|]'
    tainted_1 = re.sub(pattern, '', tainted_0)



    os.system('ls ' + tainted_1)


if __name__ == '__main__':
        main()
