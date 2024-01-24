'''
magnitude is minimum - 1 byte overflow
no filtering
Kratkiewicz 064: inter-procedural, function pointer local control flow
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


def main():

    tainted_0 = 10

    tainted_1 = tainted_0

    # No filtering (sanitization)
    tainted_1 = tainted_0


    buf = [i for i in range(10)]

    def function1(buffer):
        #flaw
        buffer[tainted_1] = 'A'

    fptr = function1

    fptr(buf)
    print(buf)


if __name__ == '__main__':
        main()
