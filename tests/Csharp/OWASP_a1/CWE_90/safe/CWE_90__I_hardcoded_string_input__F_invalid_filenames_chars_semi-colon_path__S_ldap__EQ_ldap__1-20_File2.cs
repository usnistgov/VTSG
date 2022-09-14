
                /*
                Hardcoded string input
filtering : remove semi-colon and all invalid filenames and chars in paths
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
                using System.IO;
using System.Text.RegularExpressions;
                namespace default_namespace{
                    class Class_50878{
                        string var_50878;
                        public Class_50878(string tainted_2_50878){
                            var_50878 = tainted_2_50878;
                        }
                        public string get_var_50878(){
                            string tainted_2 = null;
            string tainted_3 = null;

                            tainted_2 = var_50878;
                            
                string regexSearch = new string(Path.GetInvalidFileNameChars()) + new string(Path.GetInvalidPathChars()) + ";";
                Regex r = new Regex(string.Format("[{0}]", Regex.Escape(regexSearch)));
                tainted_3 = r.Replace(tainted_2, "");
            
                            return tainted_3;
                        }
                        
                    }
                }
