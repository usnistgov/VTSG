'''
  Test 2 of 3 for statement_terminator
  Null string for statement_terminator
'''
'''
Hardcoded string input
no filtering
sink: check if a file exists
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

def main():
        tainted_2 = None
        tainted_3 = None

        
        tainted_2 = "hardcoded"
            
        tainted_3 = tainted_2
        
if(1==1):
    {}
elif(not 1==1):
    {}
else:
    
        
        # No filtering (sanitization)
        tainted_3 = tainted_2
        
            
        
                
        print(os.path.exists(tainted_3))
                
            
main()
