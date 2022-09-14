
                /*
                Command line args
Xpath replace char
sink : LDAP Query
LDAP Query
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
                    class Class_52543{
                        string var_52543;
                        public Class_52543(string tainted_2_52543){
                            var_52543 = tainted_2_52543;
                        }
                        public string get_var_52543(){
                            string tainted_2 = null;
            string tainted_3 = null;

                            tainted_2 = var_52543;
                            
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
