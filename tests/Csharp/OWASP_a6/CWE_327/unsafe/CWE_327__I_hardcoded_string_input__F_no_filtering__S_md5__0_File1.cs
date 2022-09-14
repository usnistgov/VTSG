
/*
Hardcoded string input
no filtering
sink : md5 function
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
using System.Security.Cryptography;
using System.Text;

namespace default_namespace{
    class MainClass26643{
        public static void Main(string[] args){
            string tainted_0 = null;
            string tainted_1 = null;

            
                tainted_0 = "hardcoded";
            
            tainted_1 = tainted_0;
            
                //No filtering (sanitization)
                tainted_1 = tainted_0;
            
            
                //flaw
                using (MD5 md5Hash = MD5.Create())
                {
                    byte[] data = md5Hash.ComputeHash(Encoding.UTF8.GetBytes(tainted_1));

                    // Create a new Stringbuilder to collect the bytes
                    // and create a string.
                    StringBuilder sBuilder = new StringBuilder();

                    // Loop through each byte of the hashed data
                    // and format each one as a hexadecimal string.
                    for (int i = 0; i < data.Length; i++)
                    {
                        sBuilder.Append(data[i].ToString("x2"));
                    }

                    string hash = sBuilder.ToString();
                }
            
            
        }
        
    }
}
