/*
input : shell commands
no filtering
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
using Npgsql;
using System;
using System.Data;
using System.Diagnostics;
using System.IO;
using System.Linq;

namespace default_namespace{
    class MainClass1{
        public static void Main(string[] args){
            string tainted_0 = null;
            string tainted_1 = null;

            
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
            
            
                //No filtering (sanitization)
                tainted_1 = tainted_0;
            
            
                //flaw
                string query = "SELECT * FROM '" + tainted_1 + "'";
            
            
            string connectionString = "Server=localhost;port=1337;User Id=postgre_user;Password=postgre_password;Database=dbname";
            NpgsqlConnection dbConnection = null;
            try{
                dbConnection = new NpgsqlConnection(connectionString);
                dbConnection.Open();
                NpgsqlCommand cmd = new NpgsqlCommand(query, dbConnection);
                NpgsqlDataReader dr = cmd.ExecuteReader();
                while (dr.Read()){
                    Console.Write("{0}\n", dr[0]);
                }
                dbConnection.Close();
            }catch (Exception e){
                Console.WriteLine(e.ToString());
            }
        
        }
        
    }
}
