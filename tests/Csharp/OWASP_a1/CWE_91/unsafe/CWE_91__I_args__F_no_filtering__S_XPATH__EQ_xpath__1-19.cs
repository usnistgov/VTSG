
/*
Command line args
no filtering
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
using System.Xml;
using System.Xml.XPath;

namespace default_namespace{
    class MainClass53282{
        public static void Main(string[] args){
            string tainted_2 = null;
            string tainted_3 = null;
            string tainted_4 = null;

            
                tainted_2 = args[1];
            
            tainted_4 = tainted_2;
            
                
                //No filtering (sanitization)
                tainted_3 = tainted_2;
            
                tainted_4 = function_53281(tainted_3);
            
                //flaw
                string query = "//user[@name='" + tainted_4 + "']";
            
            
            string filename = "file.xml";
            XmlDocument document = new XmlDocument( );
            document.Load(filename);
            XmlTextWriter writer = new XmlTextWriter(Console.Out);
            writer.Formatting = Formatting.Indented;

            XmlNode node = document.SelectSingleNode(query);
            node.WriteTo(writer);

            writer.Close( );
        
        }
        
                public static string function_53281(string param_53281 ){
                    return param_53281 ;
                }


    }
}
