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
using System.IO;
using System.Text.RegularExpressions;

namespace default_namespace{
    class MainClass2{
        public static void Main(string[] args){
            string tainted_0 = null;
            string tainted_5 = null;

            
                tainted_0 = args[0];
            
            tainted_5 = function_1(tainted_0);
            
                
                File.Exists(tainted_5);
            
            
        }
        
                public static string function_1(string param_1 ){
                    string tainted_2 = null;
            string tainted_3 = null;

                    tainted_2 = param_1;
                    
                string pattern = "^[\\.\\.\\/]+";
                Regex r = new Regex(pattern);
                tainted_3 = r.Replace(tainted_2, "");
            
                    return tainted_3;
                }
    }
}
