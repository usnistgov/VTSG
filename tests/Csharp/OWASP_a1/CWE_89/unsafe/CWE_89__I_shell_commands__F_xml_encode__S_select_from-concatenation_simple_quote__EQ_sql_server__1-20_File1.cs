
/*
input : shell commands
Xpath replace char
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
using System;
using System.Data.SqlClient;
using System.Diagnostics;
using System.IO;
using System.Text;

namespace default_namespace{
    class MainClass19606{
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
            
                Class_19605 var_19605 = new Class_19605(tainted_0);
                tainted_5 = var_19605.get_var_19605();
            
                //flaw
                string query = "SELECT * FROM '" + tainted_5 + "'";
            
            
            string connectionString =  @"server=localhost;uid=sql_user;password=sql_password;database=dbname";
            SqlConnection dbConnection = null;
            try {
                dbConnection = new SqlConnection(connectionString);
                dbConnection.Open();
                SqlCommand cmd = dbConnection.CreateCommand();
                cmd.CommandText = query;
                SqlDataReader reader = cmd.ExecuteReader();
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
