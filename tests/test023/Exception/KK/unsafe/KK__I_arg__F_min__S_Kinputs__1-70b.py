
'''
input: integer from command line arg
incorrectly filter out invalid input
Kratkiewicz 180, 181, and 182: inputs from various sources; basic write
'''


class Class_1:
    def __init__(self,tainted_2_1):
        self.var_1 = tainted_2_1
    def  get_var_1(self):

        tainted_2 = var_1

        if tainted_2 < 0 or tainted_2 > 10:
            print('Bad value')
            sys.exit(0)
        tainted_3 = tainted_2

        return tainted_3
