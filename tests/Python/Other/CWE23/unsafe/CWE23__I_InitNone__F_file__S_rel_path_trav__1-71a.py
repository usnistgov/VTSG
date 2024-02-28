'''
Initialize to None
input (filter): file data.txt
sink: open file named by input
<< POV
../etc/passwd
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
import os
import sys
# like import 'CWE23__I_InitNone__F_file__S_rel_path_trav__1-71b.py' as module71
import importlib.machinery
import importlib.util
import os
import pathlib
path_to_parent = str(pathlib.Path(__file__).parent)
loader = importlib.machinery.SourceFileLoader('SFL', os.path.join(path_to_parent,
                                'CWE23__I_InitNone__F_file__S_rel_path_trav__1-71b.py'))
spec = importlib.util.spec_from_loader('SFL', loader)
module71 = importlib.util.module_from_spec(spec)
loader.exec_module(module71)


def main():

    # no input
    tainted_1 = None

    tainted_3 = tainted_1

    var_1 = module71.Class_1(tainted_1)
    tainted_2 = var_1.get_var_1()

    with open('data.txt', 'r') as f:
        tainted_3 = f.readline().rstrip() # read one line, remove newline


    if sys.platform == 'linux':
        root = '/home'
    else:
        # MacOS
        root = '/Users'

    if tainted_3 is not None:
        #flaw # no validation - concatenated value could have path traversal
        file = os.path.join(root, tainted_3)
        with open(file, 'r') as f:
            print(f.readline(), end='')

    print('Done')


if __name__ == '__main__':
        main()
