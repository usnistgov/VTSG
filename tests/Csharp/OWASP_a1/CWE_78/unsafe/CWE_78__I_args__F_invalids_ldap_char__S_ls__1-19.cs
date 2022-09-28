
/*
Command line args
filtering : remove all '\', '*', '(', ')', 'u0000', '/' in parameter
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
using System.Text;

namespace default_namespace{
    class MainClass25894{
        public static void Main(string[] args){
            string tainted_2 = null;
            string tainted_3 = null;
            string tainted_4 = null;

            
                tainted_2 = args[1];
            
            tainted_4 = tainted_2;
            
                
                StringBuilder escape = new StringBuilder();
                for (int i = 0; i < tainted_2.Length; ++i){
                    char current = tainted_2[i];
                    switch (current){
                        case '\\':
                            escape.Append(@"\5c");
                            break;
                        case '*':
                            escape.Append(@"\2a");
                            break;
                        case '(':
                            escape.Append(@"\28");
                            break;
                        case ')':
                            escape.Append(@"\29");
                            break;
                        case '\u0000':
                            escape.Append(@"\00");
                            break;
                        case '/':
                            escape.Append(@"\2f");
                            break;
                        default:
                            escape.Append(current);
                            break;
                    }
                }
                tainted_3 = escape.ToString();
            
                tainted_4 = function_25893(tainted_3);
            
                //flaw
                System.Diagnostics.Process.Start("/bin/bash", "-c 'ls " + tainted_4 + "'");
            
            
        }
        
                public static string function_25893(string param_25893 ){
                    return param_25893 ;
                }


    }
}
