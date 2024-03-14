'''
input: integer from command line arg
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
# like import 'KK__I_arg__F_ok__S_Kinputs__1-72b.py' as module72
import importlib.machinery
import importlib.util
import os
import pathlib
path_to_parent = str(pathlib.Path(__file__).parent)
loader = importlib.machinery.SourceFileLoader('SFL', os.path.join(path_to_parent,
                                'KK__I_arg__F_ok__S_Kinputs__1-72b.py'))
spec = importlib.util.spec_from_loader('SFL', loader)
module72 = importlib.util.module_from_spec(spec)
loader.exec_module(module72)


def main():

    try:
        tainted_2 = int(sys.argv[1])
    except ValueError:
        tainted_2 = 1776



    if tainted_2 < 0 or tainted_2 > 9:
        print('Bad value')
        sys.exit(0)
    tainted_3 = tainted_2

    var_1 = module72.Class_1(tainted_3)
    tainted_4 = var_1.get_var_1()

    buf = [i for i in range(10)]


    buf[tainted_4] = 'A'
    print(buf)


if __name__ == '__main__':
        main()
