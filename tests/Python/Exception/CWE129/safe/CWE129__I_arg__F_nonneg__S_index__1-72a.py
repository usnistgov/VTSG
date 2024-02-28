'''
input: integer from command line arg
filter: block inputs less than 0

<< POV
-6
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
import sys
# like import 'CWE129__I_arg__F_nonneg__S_index__1-72b.py' as module72
import importlib.machinery
import importlib.util
import os
import pathlib
path_to_parent = str(pathlib.Path(__file__).parent)
loader = importlib.machinery.SourceFileLoader('SFL', os.path.join(path_to_parent,
                                'CWE129__I_arg__F_nonneg__S_index__1-72b.py'))
spec = importlib.util.spec_from_loader('SFL', loader)
module72 = importlib.util.module_from_spec(spec)
loader.exec_module(module72)


def main():

    try:
        tainted_2 = int(sys.argv[1])
    except ValueError:
        tainted_2 = 1776

    tainted_4 = tainted_2


    if tainted_2 < 0:
        sys.exit("Negative input not allowed")
    tainted_3 = tainted_2

    var_1 = module72.Class_1(tainted_3)
    tainted_4 = var_1.get_var_1()

    array = [0, 1, 2, 3, 4]

    # check that tainted_4 < len(array), but not that it is >= 0, so may attempt to read out of array bounds
    if tainted_4 < len(array):
        print(array[tainted_4])
    else:
        print('Array index out of bounds')

    print('Done')


if __name__ == '__main__':
        main()
