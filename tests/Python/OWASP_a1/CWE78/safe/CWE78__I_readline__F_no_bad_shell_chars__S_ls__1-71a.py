'''
input: direct user input in string
filter: remove all shell list or pipe operators
sink: run ls in a dir
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
# like import 'CWE78__I_readline__F_no_bad_shell_chars__S_ls__1-71b.py' as module71
import importlib.machinery
import importlib.util
import os
import pathlib
path_to_parent = str(pathlib.Path(__file__).parent)
loader = importlib.machinery.SourceFileLoader('SFL', os.path.join(path_to_parent,
                                'CWE78__I_readline__F_no_bad_shell_chars__S_ls__1-71b.py'))
spec = importlib.util.spec_from_loader('SFL', loader)
module71 = importlib.util.module_from_spec(spec)
loader.exec_module(module71)
import os
import re


def main():
    tainted_1 = input()

    var_1 = module71.Class_1(tainted_1)
    tainted_2 = var_1.get_var_1()

    # remove ||, &&, ;, &, and |
    pattern = '\|\||&&|[;&|]'
    tainted_3 = re.sub(pattern, '', tainted_2)



    os.system('ls ' + tainted_3)


if __name__ == '__main__':
        main()
