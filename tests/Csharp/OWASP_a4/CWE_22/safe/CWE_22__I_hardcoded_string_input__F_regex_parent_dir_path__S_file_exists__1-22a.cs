
/*
Hardcoded string input
filtering : remove first "../" in path
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
    class MainClass3515{
        public static void Main(string[] args){
            string tainted_2 = null;
            string tainted_3 = null;
            string tainted_4 = null;

            
                tainted_2 = "hardcoded";
            
            tainted_4 = tainted_2;
            
                
                string pattern = "^\\.\\.\\/";
                Regex r = new Regex(pattern);
                tainted_3 = r.Replace(tainted_2, "");
            
                Class_3514 var_3514 = new Class_3514(tainted_3);
                tainted_4 = var_3514.get_var_3514();
            
                
                File.Exists(tainted_4);
            
            
        }
        
    }
}
