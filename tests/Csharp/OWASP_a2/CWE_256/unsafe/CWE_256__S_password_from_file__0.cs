
/*
sink : connection to a database using hardcoded password in a file
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
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;

namespace default_namespace{
    class MainClass1{
        public static void Main(string[] args){
            
            
            
            
                var data = new Dictionary<string, string>();
                foreach (var row in File.ReadAllLines("./config.properties"))
                    data.Add(row.Split('=')[0], string.Join("=",row.Split('=').Skip(1).ToArray()));

                Console.WriteLine(data["username"]);
                //flaw
                Console.WriteLine(data["password"]);
                string connectionString = @"server=localhost;uid=" + data["username"] + ";password=" + data["password"] + ";database=dbname";
                MySqlConnection dbConnection = null;

                try {
                    dbConnection = new MySqlConnection(connectionString);
                    dbConnection.Open();

                    dbConnection.Close();

                } catch (Exception e) {
                    Console.WriteLine(e.ToString());
                }
            
            
        }
        
    }
}
