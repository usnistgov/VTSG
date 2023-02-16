
'''
Initialize to None
input (filter): file data.txt
sink: open file named by input
<< POV
../etc/passwd
POV
'''


class Class_1:
    def __init__(self,tainted_2_1):
        self.var_1 = tainted_2_1
    def  get_var_1(self):

        tainted_2 = var_1

        with open('data.txt', 'r') as f:
            tainted_3 = f.readline().rstrip() # read one line, remove newline

        return tainted_3
