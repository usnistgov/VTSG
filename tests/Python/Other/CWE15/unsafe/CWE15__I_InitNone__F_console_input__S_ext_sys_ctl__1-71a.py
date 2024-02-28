'''
Initialize to None
input (filter): stdin << INPUT
../etc/passwd
INPUT
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
import sys
# like import 'CWE15__I_InitNone__F_console_input__S_ext_sys_ctl__1-71b.py' as module71
import importlib.machinery
import importlib.util
import os
import pathlib
path_to_parent = str(pathlib.Path(__file__).parent)
loader = importlib.machinery.SourceFileLoader('SFL', os.path.join(path_to_parent,
                                'CWE15__I_InitNone__F_console_input__S_ext_sys_ctl__1-71b.py'))
spec = importlib.util.spec_from_loader('SFL', loader)
module71 = importlib.util.module_from_spec(spec)
loader.exec_module(module71)


def main():

    # no input
    tainted_1 = None

    tainted_3 = tainted_1

    var_1 = module71.Class_1(tainted_1)
    tainted_2 = var_1.get_var_1()

    tainted_3 = input() # read one line


    if tainted_3 is not None:
        #flaw # no validation - concatenated value allows arbitrary execution
        sys.path += [tainted_3]
        print(f'added { tainted_3 } to Python module search path')

    print('Finished')


if __name__ == '__main__':
        main()
