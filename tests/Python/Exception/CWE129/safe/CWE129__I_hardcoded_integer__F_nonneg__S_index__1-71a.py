'''
Hardcoded integer as input
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
# like import 'CWE129__I_hardcoded_integer__F_nonneg__S_index__1-71b.py' as module71
import importlib.machinery
import importlib.util
import os
import pathlib
path_to_parent = str(pathlib.Path(__file__).parent)
loader = importlib.machinery.SourceFileLoader('SFL', os.path.join(path_to_parent,
                                'CWE129__I_hardcoded_integer__F_nonneg__S_index__1-71b.py'))
spec = importlib.util.spec_from_loader('SFL', loader)
module71 = importlib.util.module_from_spec(spec)
loader.exec_module(module71)


def main():
    tainted_1 = 0

    var_1 = module71.Class_1(tainted_1)
    tainted_2 = var_1.get_var_1()

    if tainted_2 < 0:
        sys.exit("Negative input not allowed")
    tainted_3 = tainted_2


    array = [0, 1, 2, 3, 4]

    # check that tainted_3 < len(array), but not that it is >= 0, so may attempt to read out of array bounds
    if tainted_3 < len(array):
        print(array[tainted_3])
    else:
        print('Array index out of bounds')

    print('Done')


if __name__ == '__main__':
        main()
