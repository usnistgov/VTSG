/*
Command line args
filtering : remove semi-colon and all invalid filenames and chars in paths
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
using System.IO;
using System.Text.RegularExpressions;
using System.Xml;
using System.Xml.XPath;

namespace default_namespace{
    class MainClass2{
        public static void Main(string[] args){
            string tainted_1 = null;
            string tainted_2 = null;
            string tainted_3 = null;

            
                tainted_1 = args[1];
            
            
                string[] arr_1 = new string[4]; // declaring array
                //Storing value in array element
                arr_1[0] = null;
                arr_1[1] = null;
                arr_1[2] = null;
                arr_1[3] = tainted_1;
                foreach(string val_1 in arr_1){
                    if(val_1!=null){
                        tainted_2 = val_1;
                        
                string regexSearch = new string(Path.GetInvalidFileNameChars()) + new string(Path.GetInvalidPathChars()) + ";";
                Regex r = new Regex(string.Format("[{0}]", Regex.Escape(regexSearch)));
                tainted_3 = r.Replace(tainted_2, "");
            
                    }
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
