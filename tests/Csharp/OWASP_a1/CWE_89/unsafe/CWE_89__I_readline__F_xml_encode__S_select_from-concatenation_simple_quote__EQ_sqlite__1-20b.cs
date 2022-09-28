
                /*
                input : direct user input in string
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
                using System.Text;
                namespace default_namespace{
                    class Class_20900{
                        string var_20900;
                        public Class_20900(string tainted_2_20900){
                            var_20900 = tainted_2_20900;
                        }
                        public string get_var_20900(){
                            string tainted_2 = null;
            string tainted_3 = null;

                            tainted_2 = var_20900;
                            
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
