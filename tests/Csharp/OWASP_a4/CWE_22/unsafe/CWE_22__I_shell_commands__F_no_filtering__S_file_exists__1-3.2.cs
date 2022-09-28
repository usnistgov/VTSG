
/*
input : shell commands
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
using System.Diagnostics;
using System.IO;

namespace default_namespace{
    class MainClass37{
        public static void Main(string[] args){
            string tainted_2 = null;
            string tainted_3 = null;

            
                Process process = new Process();
                process.StartInfo.FileName = "/bin/bash";
                process.StartInfo.Arguments = "-c 'cat /tmp/tainted.txt'";
                process.StartInfo.UseShellExecute = false;
                process.StartInfo.RedirectStandardOutput = true;
                process.Start();

                using(StreamReader reader = process.StandardOutput) {
                    tainted_2 = reader.ReadToEnd();
                    process.WaitForExit();
                    process.Close();
                }
            
            tainted_3 = tainted_2;
            
                if((1==0)){
                    {}
                }else{
                    
                //No filtering (sanitization)
                tainted_3 = tainted_2;
            
                }
            
                //flaw
                File.Exists(tainted_3);
            
            
        }
        
    }
}
