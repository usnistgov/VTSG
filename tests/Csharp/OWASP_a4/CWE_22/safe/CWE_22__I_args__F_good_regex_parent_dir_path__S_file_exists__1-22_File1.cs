
/*
Command line args
filtering : remove all "../" in path
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
using System.Text.RegularExpressions;

namespace default_namespace{
    class MainClass4440{
        public static void Main(string[] args){
            string tainted_2 = null;
            string tainted_3 = null;
            string tainted_4 = null;

            
                tainted_2 = args[1];
            
            tainted_4 = tainted_2;
            
                
                string pattern = "^[\\.\\.\\/]+";
                Regex r = new Regex(pattern);
                tainted_3 = r.Replace(tainted_2, "");
            
                Class_4439 var_4439 = new Class_4439(tainted_3);
                tainted_4 = var_4439.get_var_4439();
            
                
                File.Exists(tainted_4);
            
            
        }
        
    }
}
