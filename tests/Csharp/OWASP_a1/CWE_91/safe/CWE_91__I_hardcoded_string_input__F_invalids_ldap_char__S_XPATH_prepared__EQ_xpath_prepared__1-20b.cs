
                /*
                Hardcoded string input
filtering : remove all '\', '*', '(', ')', 'u0000', '/' in parameter
sink : XPATH prepared
exec_query : xpath prepared statement
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
                using System.Text;
                namespace default_namespace{
                    class Class_62718{
                        string var_62718;
                        public Class_62718(string tainted_2_62718){
                            var_62718 = tainted_2_62718;
                        }
                        public string get_var_62718(){
                            string tainted_2 = null;
            string tainted_3 = null;

                            tainted_2 = var_62718;
                            
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
            
                            return tainted_3;
                        }
                        
                    }
                }
