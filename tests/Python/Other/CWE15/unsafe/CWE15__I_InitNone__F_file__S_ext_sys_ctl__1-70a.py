'''
Initialize to None
input (filter): file data.txt
sink: add directory named by input to Python module search path
<< POV
.
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
# like import 'CWE15__I_InitNone__F_file__S_ext_sys_ctl__1-70b.py' as module70
import importlib.machinery
import importlib.util
import os
import pathlib
path_to_parent = str(pathlib.Path(__file__).parent)
loader = importlib.machinery.SourceFileLoader('SFL', os.path.join(path_to_parent,
                                'CWE15__I_InitNone__F_file__S_ext_sys_ctl__1-70b.py'))
spec = importlib.util.spec_from_loader('SFL', loader)
module70 = importlib.util.module_from_spec(spec)
loader.exec_module(module70)
import sys


def main():

    # no input
    tainted_0 = None


    var_1 = module70.Class_1(tainted_0)
    tainted_5 = var_1.get_var_1()

    if tainted_5 is not None:
        #flaw # no validation - concatenated value allows arbitrary execution
        sys.path += [tainted_5]
        print(f'added { tainted_5 } to Python module search path')

    print('Finished')


if __name__ == '__main__':
        main()
