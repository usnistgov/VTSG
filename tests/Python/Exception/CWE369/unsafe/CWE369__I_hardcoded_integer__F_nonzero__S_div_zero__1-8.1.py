'''
Hardcoded integer as input
filter: block zero arguments
sink: divide by input
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


def main():
    tainted_2 = 0
    tainted_3 = tainted_2

    if 1==1:
        pass
    elif not 1==1:
        pass
    else:

        if tainted_2 == 0:
            sys.exit("Zero input not allowed")
        tainted_3 = tainted_2


    user_input = tainted_3
    #flaw
    print(f'The reciprocal of {user_input} is {1/user_input}')


if __name__ == '__main__':
        main()
