'''
input: direct user input in string
no filtering
sink: loop condition from input - unchecked
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
    tainted_0 = input()

    # No filtering (sanitization)
    tainted_1 = tainted_0


    # convert input string to number
    try:
        number_of_loops = int(tainted_1)
    except ValueError:
        print('Invalid input.  Numeric input expected.  Assuming 1.')
        number_of_loops = 1

    #flaw
    for j in range(number_of_loops):
        print('Hello, world')


if __name__ == '__main__':
        main()
