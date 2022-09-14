
                /*
                input : direct user input in string
filtering : remove first "../" in path
sink : check if a file exists
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
                using System.Text.RegularExpressions;
                namespace default_namespace{
                    class Class_3325{
                        string var_3325;
                        public Class_3325(string tainted_2_3325){
                            var_3325 = tainted_2_3325;
                        }
                        public string get_var_3325(){
                            string tainted_2 = null;
            string tainted_3 = null;

                            tainted_2 = var_3325;
                            
                string pattern = "^\\.\\.\\/";
                Regex r = new Regex(pattern);
                tainted_3 = r.Replace(tainted_2, "");
            
                            return tainted_3;
                        }
                        
                    }
                }
