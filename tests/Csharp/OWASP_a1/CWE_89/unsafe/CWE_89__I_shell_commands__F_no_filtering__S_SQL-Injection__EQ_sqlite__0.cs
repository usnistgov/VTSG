/*
input : shell commands
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
using System.Diagnostics;
using System.IO;

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
                string query = "SELECT * FROM Articles WHERE id="+tainted_1;
            
            
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
        
    }
}
