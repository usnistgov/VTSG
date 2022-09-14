
/*
Hardcoded string input
Xpath replace char
sink : SQL query
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
using System.Data.OracleClient;
using System.Text;

namespace default_namespace{
    class MainClass44213{
        public static void Main(string[] args){
            string tainted_0 = null;
            string tainted_5 = null;

            
                tainted_0 = "hardcoded";
            
            tainted_5 = tainted_0;
            tainted_5 = function_44212(tainted_0);
            
                
                string query = "SELECT * FROM Articles WHERE id="+tainted_5;
            
            
            string connectionString = "Data Source=localhost;User ID=oracle_user;Password=oracle_password";
            OracleConnection dbConnection = null;
            try{
                dbConnection = new OracleConnection(connectionString);
                dbConnection.Open();
                OracleCommand cmd = dbConnection.CreateCommand();
                cmd.CommandText = query;
                OracleDataReader reader = cmd.ExecuteReader();
                while (reader.Read()){
                    Console.WriteLine(reader.ToString());
                }
                dbConnection.Close();
            }catch(Exception e){
                Console.WriteLine(e.ToString());
            }
        
        }
        
                public static string function_44212(string param_44212 ){
                    string tainted_2 = null;
            string tainted_3 = null;

                    tainted_2 = param_44212;
                    
                StringBuilder text = new StringBuilder(tainted_2);
                text.Replace("&", "&amp;");
                text.Replace("'", "&apos;");
                text.Replace(@"""", "&quot;");
                text.Replace("<", "&lt;");
                text.Replace(">", "&gt;");
                tainted_3 = text.ToString();
            
                    return tainted_3;
                }
    }
}
