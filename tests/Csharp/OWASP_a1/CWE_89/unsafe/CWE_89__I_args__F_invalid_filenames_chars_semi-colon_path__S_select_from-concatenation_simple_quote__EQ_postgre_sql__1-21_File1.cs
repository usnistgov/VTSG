
/*
Command line args
filtering : remove semi-colon and all invalid filenames and chars in paths
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
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;

namespace default_namespace{
    class MainClass15168{
        public static void Main(string[] args){
            string tainted_1 = null;
            string tainted_2 = null;
            string tainted_3 = null;

            
                tainted_1 = args[1];
            
            tainted_3 = tainted_1;
            
                Class_15167 var_15167 = new Class_15167(tainted_1);
                tainted_2 = var_15167.get_var_15167();
                
                string regexSearch = new string(Path.GetInvalidFileNameChars()) + new string(Path.GetInvalidPathChars()) + ";";
                Regex r = new Regex(string.Format("[{0}]", Regex.Escape(regexSearch)));
                tainted_3 = r.Replace(tainted_2, "");
            
            
                //flaw
                string query = "SELECT * FROM '" + tainted_3 + "'";
            
            
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
