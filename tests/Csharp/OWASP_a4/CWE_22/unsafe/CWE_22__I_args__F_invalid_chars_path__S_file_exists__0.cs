/*
Command line args
filtering : remove all invalid chars in a path
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
    class MainClass1{
        public static void Main(string[] args){
            string tainted_0 = null;
            string tainted_1 = null;

            
                tainted_0 = args[1];
            
            tainted_1 = tainted_0;
            
                string regexSearch = new string(Path.GetInvalidPathChars());
                Regex r = new Regex(string.Format("[{0}]", Regex.Escape(regexSearch)));
                tainted_1 = r.Replace(tainted_0, "");
            
            
                //flaw
                File.Exists(tainted_1);
            
            
        }
        
    }
}
