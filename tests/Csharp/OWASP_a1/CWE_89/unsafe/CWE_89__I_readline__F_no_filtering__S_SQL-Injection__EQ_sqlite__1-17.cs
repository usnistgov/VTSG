
/*
input : direct user input in string
no filtering
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

namespace default_namespace{
    class MainClass28303{
        public static void Main(string[] args){
            string tainted_0 = null;
            string tainted_5 = null;

            
                tainted_0 = Console.ReadLine();
            
            tainted_5 = tainted_0;
            tainted_5 = function_28302(tainted_0);
            
                //flaw
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
        
                public static string function_28302(string param_28302 ){
                    string tainted_2 = null;
            string tainted_3 = null;

                    tainted_2 = param_28302;
                    
                //No filtering (sanitization)
                tainted_3 = tainted_2;
            
                    return tainted_3;
                }
    }
}
