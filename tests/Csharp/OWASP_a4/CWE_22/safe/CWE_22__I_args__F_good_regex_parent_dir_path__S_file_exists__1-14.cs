
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
    class MainClass2{
        public static void Main(string[] args){
            string tainted_1 = null;
            string tainted_2 = null;
            string tainted_3 = null;

            
                tainted_1 = args[1];
            
            tainted_3 = tainted_1;
            
                string[] arr_1 = new string[4]; // declaring array
                //Storing value in array element
                arr_1[0] = null;
                arr_1[1] = null;
                arr_1[2] = null;
                arr_1[3] = tainted_1;
                foreach(string val_1 in arr_1){
                    if(val_1!=null){
                        tainted_2 = val_1;
                        
                string pattern = "^[\\.\\.\\/]+";
                Regex r = new Regex(pattern);
                tainted_3 = r.Replace(tainted_2, "");
            
                    }
                }
            
                
                File.Exists(tainted_3);
            
            
        }
        
    }
}
