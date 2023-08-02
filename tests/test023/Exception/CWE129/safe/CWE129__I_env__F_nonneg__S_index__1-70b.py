
'''
input: integer from environment variable
filter: block inputs less than 0

<< POV
-6
POV
'''
import sys


class Class_1:
    def __init__(self,tainted_2_1):
        self.var_1 = tainted_2_1
    def  get_var_1(self):

        tainted_2 = var_1

        if tainted_2 < 0:
            sys.exit("Negative input not allowed")
        tainted_3 = tainted_2

        return tainted_3
