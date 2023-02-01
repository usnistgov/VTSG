/*
input : shell commands
filtering : remove all '\', '*', '(', ')', 'u0000', '/' in parameter
sink : XPATH Query
exec_query : xpath
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
using System.Text;
using System.Xml;
using System.Xml.XPath;

namespace default_namespace{
    class MainClass2{
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
            
                if((4+2>=42)){
                    
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
            
                }else if(!(4+2>=42)){
                    {}
                }else{
                    {}
                }
            
                //flaw
                string query = "//user[@name='" + tainted_3 + "']";
            
            
            string filename = "file.xml";
            XmlDocument document = new XmlDocument( );
            document.Load(filename);
            XmlTextWriter writer = new XmlTextWriter(Console.Out);
            writer.Formatting = Formatting.Indented;

            XmlNode node = document.SelectSingleNode(query);
            node.WriteTo(writer);

            writer.Close( );
        
        }
        
    }
}
