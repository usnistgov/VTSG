'''
input: integer from environment variable
incorrectly filter out invalid input
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
import os
import sys
# like import 'KK__I_env__F_min__S_Kinputs__1-71b.py' as module71
import importlib.machinery
import importlib.util
import os
import pathlib
path_to_parent = str(pathlib.Path(__file__).parent)
loader = importlib.machinery.SourceFileLoader('SFL', os.path.join(path_to_parent,
                                'KK__I_env__F_min__S_Kinputs__1-71b.py'))
spec = importlib.util.spec_from_loader('SFL', loader)
module71 = importlib.util.module_from_spec(spec)
loader.exec_module(module71)


def main():

    try:
        tainted_1 = int(os.environ['ADD'])
    except ValueError:
        tainted_1 = 1776

    tainted_3 = tainted_1

    var_1 = module71.Class_1(tainted_1)
    tainted_2 = var_1.get_var_1()

    if tainted_2 < 0 or tainted_2 > 10:
        print('Bad value')
        sys.exit(0)
    tainted_3 = tainted_2


    buf = [i for i in range(10)]

    #flaw
    buf[tainted_3] = 'A'
    print(buf)


if __name__ == '__main__':
        main()
