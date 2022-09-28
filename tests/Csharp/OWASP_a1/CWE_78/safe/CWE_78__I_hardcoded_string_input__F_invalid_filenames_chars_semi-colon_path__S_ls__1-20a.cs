
/*
Hardcoded string input
filtering : remove semi-colon and all invalid filenames and chars in paths
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
using System.Text.RegularExpressions;

namespace default_namespace{
    class MainClass24971{
        public static void Main(string[] args){
            string tainted_0 = null;
            string tainted_5 = null;

            
                tainted_0 = "hardcoded";
            
            tainted_5 = tainted_0;
            
                Class_24970 var_24970 = new Class_24970(tainted_0);
                tainted_5 = var_24970.get_var_24970();
            
                
                System.Diagnostics.Process.Start("/bin/bash", "-c 'ls " + tainted_5 + "'");
            
            
        }
        
    }
}
