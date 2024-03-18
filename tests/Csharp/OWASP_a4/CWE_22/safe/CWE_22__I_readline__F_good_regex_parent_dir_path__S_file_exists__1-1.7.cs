/*
input : direct user input in string
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
            string tainted_2 = null;
            string tainted_3 = null;

            
                tainted_2 = Console.ReadLine();
            
            
                if((Math.Sqrt(42)<=42)){
                    
                string pattern = "^[\\.\\.\\/]+";
                Regex r = new Regex(pattern);
                tainted_3 = r.Replace(tainted_2, "");
            
                }
            
                
                File.Exists(tainted_3);
            
            
        }
        
    }
}
