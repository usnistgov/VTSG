
/*
input : direct user input in string
no filtering
sink : XPATH prepared
exec_query : xpath prepared statement
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
using System.Linq;
using System.Xml;
using System.Xml.Linq;

namespace default_namespace{
    class MainClass60318{
        public static void Main(string[] args){
            string tainted_2 = null;
            string tainted_3 = null;
            string tainted_4 = null;

            
                tainted_2 = Console.ReadLine();
            
            tainted_4 = tainted_2;
            
                
                //No filtering (sanitization)
                tainted_3 = tainted_2;
            
                Class_60317 var_60317 = new Class_60317(tainted_3);
                tainted_4 = var_60317.get_var_60317();
            
                
                string query = tainted_4;
            
            
            string filename = "file.xml";
            XDocument document = XDocument.Load(filename);
            XmlTextWriter writer = new XmlTextWriter(Console.Out);
            writer.Formatting = Formatting.Indented;
            var node = document.Root.Elements("foo")
                   .Where(x => (string) x.Element("bar") == query)
                   .SingleOrDefault();
            node.WriteTo(writer);
            writer.Close( );
        
        }
        
    }
}
