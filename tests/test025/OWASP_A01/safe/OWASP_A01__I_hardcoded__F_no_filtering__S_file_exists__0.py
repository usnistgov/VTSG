'''
input: hard coded string
no filtering
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


def main():
    tainted_0 = 'hardcoded'

    # No filtering (sanitization)
    tainted_1 = tainted_0


    print(f'file "{ tainted_1 }" ', end='')

    if os.path.exists(tainted_1):
        print('exists')
    else:
        print('does not exist')


if __name__ == '__main__':
        main()
