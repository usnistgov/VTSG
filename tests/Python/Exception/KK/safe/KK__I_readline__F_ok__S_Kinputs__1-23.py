'''
input: integer from user input
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

    try:
        tainted_1 = int(input())
    except ValueError:
        tainted_1 = 1776


    # Declaring an array
    arr_1 = []
    # Storing value in array element
    arr_1.append(None)
    arr_1.append(None)
    arr_1.append(None)
    assert tainted_1 is not None, 'code only executed when tainted_1 != None'
    arr_1.append(tainted_1)
    for val_1 in arr_1:
        if val_1!=None:
            tainted_2 = val_1

            if tainted_2 < 0 or tainted_2 > 9:
                print('Bad value')
                sys.exit(0)
            tainted_3 = tainted_2


    buf = [i for i in range(10)]


    buf[tainted_3] = 'A'
    print(buf)


if __name__ == '__main__':
        main()
