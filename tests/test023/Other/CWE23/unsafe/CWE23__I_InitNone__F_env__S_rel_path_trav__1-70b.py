
'''
Initialize to None
input (filter): environment variable ADD << INPUT
../etc/passwd
INPUT
sink: open file named by input
<< POV
../etc/passwd
POV
'''
import os


class Class_1:
    def __init__(self,tainted_2_1):
        self.var_1 = tainted_2_1
    def  get_var_1(self):

        tainted_2 = var_1

        tainted_3 = os.environ['ADD']

        return tainted_3
