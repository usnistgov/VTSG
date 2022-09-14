
/*
Hardcoded string input
filtering : remove all '\', '*', '(', ')', 'u0000', '/' in parameter
sink : run ls in a dir
*/
/*
Created by Paul E. Black and William Mentzer 2020

This software was developed at the National Institute of Standards and Technology
by employees of the Federal Government in the course of their official duties.
Pursuant to title 17 Section 105 of the United States Code the software is not
subject to copyright protection and are in the public domain.

We would appreciate acknowledgment if the software is used.

Paul E. Black  paul.black@nist.gov
William Mentzer willmentzer20@gmail.com

*/
using System;
using System.IO;
using System.Text;

namespace default_namespace{
    class MainClass25711{
        public static void Main(string[] args){
            string tainted_0 = null;
            string tainted_5 = null;

            
                tainted_0 = "hardcoded";
            
            tainted_5 = tainted_0;
            
                Class_25710 var_25710 = new Class_25710(tainted_0);
                tainted_5 = var_25710.get_var_25710();
            
                
                System.Diagnostics.Process.Start("/bin/bash", "-c 'ls " + tainted_5 + "'");
            
            
        }
        
    }
}
