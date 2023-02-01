/*
Command line args
Xpath replace char
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
using System.Text;
using System.Xml;
using System.Xml.XPath;

namespace default_namespace{
    class MainClass2{
        public static void Main(string[] args){
            string tainted_0 = null;
            string tainted_5 = null;

            
                tainted_0 = args[1];
            
            tainted_5 = tainted_0;
            
                Class_1 var_1 = new Class_1(tainted_0);
                tainted_5 = var_1.get_var_1();
            
                
                string query = string.Format("//user[@name='{0}']",tainted_5);
            
            
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
