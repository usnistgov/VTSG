/*
Command line args
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
using Npgsql;
using System;
using System.Data;
using System.Linq;
using System.Text;

namespace default_namespace{
    class MainClass2{
        public static void Main(string[] args){
            string tainted_2 = null;
            string tainted_3 = null;

            
                tainted_2 = args[1];
            
            tainted_3 = tainted_2;
            
                if((Math.Pow(4, 2)<=42)){
                    {}
                }else if(!(Math.Pow(4, 2)<=42)){
                    {}
                }else{
                    
                StringBuilder text = new StringBuilder(tainted_2);
                text.Replace("&", "&amp;");
                text.Replace("'", "&apos;");
                text.Replace(@"""", "&quot;");
                text.Replace("<", "&lt;");
                text.Replace(">", "&gt;");
                tainted_3 = text.ToString();
            
                }
            
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
