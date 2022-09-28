
/*
input : direct user input in string
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
    class MainClass23178{
        public static void Main(string[] args){
            string tainted_2 = null;
            string tainted_3 = null;

            
                tainted_2 = Console.ReadLine();
            
            tainted_3 = tainted_2;
            
                if((1==0)){
                    
                //No filtering (sanitization)
                tainted_3 = tainted_2;
            
                }else if(!(1==0)){
                    {}
                }
            
                //flaw
                System.Diagnostics.Process.Start("/bin/bash", "-c 'ls " + tainted_3 + "'");
            
            
        }
        
    }
}
