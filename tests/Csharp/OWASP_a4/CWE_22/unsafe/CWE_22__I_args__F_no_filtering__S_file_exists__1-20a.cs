
/*
Command line args
no filtering
sink : check if a file exists
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
    class MainClass736{
        public static void Main(string[] args){
            string tainted_0 = null;
            string tainted_5 = null;

            
                tainted_0 = args[1];
            
            tainted_5 = tainted_0;
            
                Class_735 var_735 = new Class_735(tainted_0);
                tainted_5 = var_735.get_var_735();
            
                //flaw
                File.Exists(tainted_5);
            
            
        }
        
    }
}
