
'''
Hardcoded string as input
no filtering
sink: run ls in a dir
'''


class Class_900:
    def __init__(self,tainted_2_900):
        self.var_900 = tainted_2_900
    def  get_var_900(self):
        tainted_2 = None
        tainted_3 = None

        tainted_2 = var_900

        # No filtering (sanitization)
        tainted_3 = tainted_2

        return tainted_3
