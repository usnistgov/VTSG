
/*
Hardcoded string input
filtering : check if there is only numbers
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
using System.Text.RegularExpressions;

namespace default_namespace{
    class MainClass33119{
        public static void Main(string[] args){
            string tainted_0 = null;
            string tainted_5 = null;

            
                tainted_0 = "hardcoded";
            
            tainted_5 = tainted_0;
            
                Class_33118 var_33118 = new Class_33118(tainted_0);
                tainted_5 = var_33118.get_var_33118();
            
                
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
        
    }
}
