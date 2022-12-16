
'''
input: direct user input in string
no filtering
sink: loop condition from input - checked
'''


class Class_1:
    def __init__(self,tainted_2_1):
        self.var_1 = tainted_2_1
    def  get_var_1(self):
        tainted_2 = None
        tainted_3 = None

        tainted_2 = var_1

        # No filtering (sanitization)
        tainted_3 = tainted_2

        return tainted_3
