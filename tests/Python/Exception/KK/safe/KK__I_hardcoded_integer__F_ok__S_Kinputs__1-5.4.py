'''
Hardcoded integer as input
filter out invalid input
Kratkiewicz 180, 181, and 182: inputs from various sources; basic write
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

    if (4+2>=42):
        pass
    elif not (4+2>=42):

        if tainted_2 < 0 or tainted_2 > 9:
            print('Bad value')
            sys.exit(0)
        tainted_3 = tainted_2


    buf = [i for i in range(10)]


    buf[tainted_3] = 'A'
    print(buf)


if __name__ == '__main__':
        main()
