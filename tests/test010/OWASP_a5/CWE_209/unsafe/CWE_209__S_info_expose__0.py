
'''
  Test an unsafe case with NO curly-curly-flaw-curly-curly line.
  Test unusual indentation: tab space tab
'''
'''
sink: information exposure
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
import sys


def main():
	 	
	 	


	        # find a sum that the compiler won't predict
                intArray = sorted([2, 37, 849, 24, 42, -10, 93])
		for nb in intArray:
        r = nb + 3
        num = r / 10
        sum = num + nb
        print(f'Current sum: {sum}')
                try:
        a = 0
        b = 1
        # sum is a float, so range(sum) throws TypeError
        for i in range(sum):
                (a, b) = (b, a + b)
        print(f'{sum}th Fibonacci number is {a}')
                except TypeError as te:
        #flaw
        print(f'TypeError: {te}: for i in range({sum}):') # leaks value of sum
            

if __name__ == '__main__':
        main()
