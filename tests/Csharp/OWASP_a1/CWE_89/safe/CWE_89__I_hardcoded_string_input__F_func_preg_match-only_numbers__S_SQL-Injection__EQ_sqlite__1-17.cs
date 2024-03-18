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
using System.Data;
using System.Data.SQLite;
using System.Text.RegularExpressions;

namespace default_namespace{
    class MainClass2{
        public static void Main(string[] args){
            string tainted_0 = null;
            string tainted_5 = null;

            
                tainted_0 = "hardcoded";
            
            tainted_5 = function_1(tainted_0);
            
                
                string query = "SELECT * FROM Articles WHERE id="+tainted_5;
            
            
            SQLiteConnection dbConnection = null;
            try{
                dbConnection = new SQLiteConnection("data source=C:\\data");
                SQLiteCommand command = new SQLiteCommand(query, dbConnection);
                SQLiteDataReader reader = command.ExecuteReader();
                while (reader.Read()){
                    Console.WriteLine(reader.ToString());
                }
                dbConnection.Close();
            }catch(Exception e){
                Console.WriteLine(e.ToString());
            }
        
        }
        
                public static string function_1(string param_1 ){
                    string tainted_2 = null;
            string tainted_3 = null;

                    tainted_2 = param_1;
                    
                string pattern = @"/^[0-9]*$/";
                Regex r = new Regex(pattern);
                Match m = r.Match(tainted_2);
                if(!m.Success){
                    tainted_3 = "";
                }else{
                    tainted_3 = tainted_2;
                }
            
                    return tainted_3;
                }
    }
}
