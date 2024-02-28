'''
input: file data.txt containing an integer
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
# like import 'CWE369__I_file__F_nonzero__S_div_zero__1-70b.py' as module70
import importlib.machinery
import importlib.util
import os
import pathlib
path_to_parent = str(pathlib.Path(__file__).parent)
loader = importlib.machinery.SourceFileLoader('SFL', os.path.join(path_to_parent,
                                'CWE369__I_file__F_nonzero__S_div_zero__1-70b.py'))
spec = importlib.util.spec_from_loader('SFL', loader)
module70 = importlib.util.module_from_spec(spec)
loader.exec_module(module70)


def main():

    try:
        with open('data.txt', 'r') as f:
            tainted_0 = int(f.readline())
    except ValueError:
        tainted_0 = 1776

    tainted_5 = tainted_0

    var_1 = module70.Class_1(tainted_0)
    tainted_5 = var_1.get_var_1()

    user_input = tainted_5

    print(f'The reciprocal of {user_input} is {1/user_input}')


if __name__ == '__main__':
        main()
