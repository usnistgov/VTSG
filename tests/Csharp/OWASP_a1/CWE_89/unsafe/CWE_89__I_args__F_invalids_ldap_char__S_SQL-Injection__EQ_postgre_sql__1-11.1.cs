/*
Command line args
filtering : remove all '\', '*', '(', ')', 'u0000', '/' in parameter
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

            
                tainted_2 = args[0];
            
            
                while((1==1)){
                    
                StringBuilder escape = new StringBuilder();
                for (int i = 0; i < tainted_2.Length; ++i){
                    char current = tainted_2[i];
                    switch (current){
                        case '\\':
                            escape.Append(@"\5c");
                            break;
                        case '*':
                            escape.Append(@"\2a");
                            break;
                        case '(':
                            escape.Append(@"\28");
                            break;
                        case ')':
                            escape.Append(@"\29");
                            break;
                        case '\u0000':
                            escape.Append(@"\00");
                            break;
                        case '/':
                            escape.Append(@"\2f");
                            break;
                        default:
                            escape.Append(current);
                            break;
                    }
                }
                tainted_3 = escape.ToString();
            
                    break;
                }
            
                //flaw
                string query = "SELECT * FROM Articles WHERE id="+tainted_3;
            
            
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
