
/*
Hardcoded string input
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
    class MainClass60493{
        public static void Main(string[] args){
            string tainted_0 = null;
            string tainted_5 = null;

            
                tainted_0 = "hardcoded";
            
            tainted_5 = tainted_0;
            tainted_5 = function_60492(tainted_0);
            
                
                string query = tainted_5;
            
            
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
        
                public static string function_60492(string param_60492 ){
                    string tainted_2 = null;
            string tainted_3 = null;

                    tainted_2 = param_60492;
                    
                //No filtering (sanitization)
                tainted_3 = tainted_2;
            
                    return tainted_3;
                }
    }
}
