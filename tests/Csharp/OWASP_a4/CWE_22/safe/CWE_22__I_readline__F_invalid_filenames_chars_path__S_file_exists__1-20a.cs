/*
input : direct user input in string
filtering : remove all invalid filenames and chars in paths
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
    class MainClass2{
        public static void Main(string[] args){
            string tainted_0 = null;
            string tainted_5 = null;

            
                tainted_0 = Console.ReadLine();
            
            
                Class_1 var_1 = new Class_1(tainted_0);
                tainted_5 = var_1.get_var_1();
            
                
                File.Exists(tainted_5);
            
            
        }
        
    }
}
