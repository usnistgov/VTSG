
                /*
                input : direct user input in string
Xpath replace char
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
                    class Class_63273{
                        string var_63273;
                        public Class_63273(string tainted_2_63273){
                            var_63273 = tainted_2_63273;
                        }
                        public string get_var_63273(){
                            string tainted_2 = null;
            string tainted_3 = null;

                            tainted_2 = var_63273;
                            
                StringBuilder text = new StringBuilder(tainted_2);
                text.Replace("&", "&amp;");
                text.Replace("'", "&apos;");
                text.Replace(@"""", "&quot;");
                text.Replace("<", "&lt;");
                text.Replace(">", "&gt;");
                tainted_3 = text.ToString();
            
                            return tainted_3;
                        }
                        
                    }
                }
