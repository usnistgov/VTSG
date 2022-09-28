
/*
Hardcoded string input
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
    class MainClass53075{
        public static void Main(string[] args){
            string tainted_2 = null;
            string tainted_3 = null;

            
                tainted_2 = "hardcoded";
            
            tainted_3 = tainted_2;
            
                do{
                    
                //No filtering (sanitization)
                tainted_3 = tainted_2;
            
                    break;
                }while((4+2>=42));
            
                
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
