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
using MySql.Data.MySqlClient;
using System;

namespace default_namespace{
    class MainClass2{
        public static void Main(string[] args){
            string tainted_0 = null;
            string tainted_5 = null;

            
                tainted_0 = "hardcoded";
            
            
                Class_1 var_1 = new Class_1(tainted_0);
                tainted_5 = var_1.get_var_1();
            
                string query = "SELECT * FROM Articles WHERE id=@placeholder";
                string checked_data = tainted_5;
            
            
            string connectionString = @"server=localhost;uid=mysql_user;password=mysql_password;database=dbname";
            MySqlConnection dbConnection = null;
            try {
                dbConnection = new MySqlConnection(connectionString);
                dbConnection.Open();
                MySqlCommand cmd = dbConnection.CreateCommand();
                cmd = new MySqlCommand(query);
                cmd.Parameters.AddWithValue("@placeholder",checked_data);
                cmd.Prepare();
                MySqlDataReader reader = cmd.ExecuteReader();
                while (reader.Read()){
                    Console.WriteLine(reader.ToString());
                }
                dbConnection.Close();
            } catch (Exception e) {
                Console.WriteLine(e.ToString());
            }
        
        }
        
    }
}
