
/*
Command line args
no filtering
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

namespace default_namespace{
    class MainClass23670{
        public static void Main(string[] args){
            string tainted_0 = null;
            string tainted_5 = null;

            
                tainted_0 = args[1];
            
            tainted_5 = tainted_0;
            tainted_5 = function_23669(tainted_0);
            
                //flaw
                System.Diagnostics.Process.Start("/bin/bash", "-c 'ls " + tainted_5 + "'");
            
            
        }
        
                public static string function_23669(string param_23669 ){
                    string tainted_2 = null;
            string tainted_3 = null;

                    tainted_2 = param_23669;
                    
                //No filtering (sanitization)
                tainted_3 = tainted_2;
            
                    return tainted_3;
                }
    }
}
