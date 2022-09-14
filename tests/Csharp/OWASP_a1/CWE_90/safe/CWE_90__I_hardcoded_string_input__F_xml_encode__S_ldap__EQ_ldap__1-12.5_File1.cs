
/*
Hardcoded string input
Xpath replace char
sink : LDAP Query
LDAP Query
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
using System.DirectoryServices;
using System.Text;

namespace default_namespace{
    class MainClass52337{
        public static void Main(string[] args){
            string tainted_2 = null;
            string tainted_3 = null;

            
                tainted_2 = "hardcoded";
            
            tainted_3 = tainted_2;
            
                do{
                    
                StringBuilder text = new StringBuilder(tainted_2);
                text.Replace("&", "&amp;");
                text.Replace("'", "&apos;");
                text.Replace(@"""", "&quot;");
                text.Replace("<", "&lt;");
                text.Replace(">", "&gt;");
                tainted_3 = text.ToString();
            
                    break;
                }while((Math.Pow(4, 2)<=42));
            
                
                string query = "(&(objectClass=person)(sn=" + tainted_3 + "))";
            
            
            string strConnect = "LDAP://my.site.com/o=site,c=com";
            using (System.DirectoryServices.DirectoryEntry CN_Main = new System.DirectoryServices.DirectoryEntry(strConnect)){
                string strResult = "";
                System.DirectoryServices.DirectorySearcher DirSearcher = new System.DirectoryServices.DirectorySearcher(CN_Main, query);
                System.DirectoryServices.DirectoryEntry CN_Result;
                CN_Main.AuthenticationType = AuthenticationTypes.None;
                foreach (System.DirectoryServices.SearchResult ResultSearch in DirSearcher.FindAll()){
                    if (ResultSearch != null){
                        CN_Result = ResultSearch.GetDirectoryEntry();
                        if ((string)CN_Result.Properties["userclass"][0] == "noname"){
                            strResult = strResult + "Name : " + CN_Result.InvokeGet("sn");
                        }
                    }
                }
                Console.WriteLine(strResult);
            }
        
        }
        
    }
}
