
/*
input : shell commands
filtering : remove all '\', '*', '(', ')', 'u0000', '/' in parameter
construction : concatenation with simple quote
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
using System.Diagnostics;
using System.IO;
using System.Text;

namespace default_namespace{
    class MainClass15721{
        public static void Main(string[] args){
            string tainted_0 = null;
            string tainted_5 = null;

            
                Process process = new Process();
                process.StartInfo.FileName = "/bin/bash";
                process.StartInfo.Arguments = "-c 'cat /tmp/tainted.txt'";
                process.StartInfo.UseShellExecute = false;
                process.StartInfo.RedirectStandardOutput = true;
                process.Start();

                using(StreamReader reader = process.StandardOutput) {
                    tainted_0 = reader.ReadToEnd();
                    process.WaitForExit();
                    process.Close();
                }
            
            tainted_5 = tainted_0;
            
                Class_15720 var_15720 = new Class_15720(tainted_0);
                tainted_5 = var_15720.get_var_15720();
            
                //flaw
                string query = "SELECT * FROM '" + tainted_5 + "'";
            
            
            string connectionString = @"server=localhost;uid=mysql_user;password=mysql_password;database=dbname";
            MySqlConnection dbConnection = null;
            try {
                dbConnection = new MySqlConnection(connectionString);
                dbConnection.Open();
                MySqlCommand cmd = dbConnection.CreateCommand();
                cmd.CommandText = query;
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
