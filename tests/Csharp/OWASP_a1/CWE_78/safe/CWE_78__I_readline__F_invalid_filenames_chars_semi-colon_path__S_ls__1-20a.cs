
/*
input : direct user input in string
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
    class MainClass24786{
        public static void Main(string[] args){
            string tainted_0 = null;
            string tainted_5 = null;

            
                tainted_0 = Console.ReadLine();
            
            tainted_5 = tainted_0;
            
                Class_24785 var_24785 = new Class_24785(tainted_0);
                tainted_5 = var_24785.get_var_24785();
            
                
                System.Diagnostics.Process.Start("/bin/bash", "-c 'ls " + tainted_5 + "'");
            
            
        }
        
    }
}
