
                /*
                Hardcoded string input
filtering : remove all "../" in path
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
                    class Class_4250{
                        string var_4250;
                        public Class_4250(string tainted_2_4250){
                            var_4250 = tainted_2_4250;
                        }
                        public string get_var_4250(){
                            string tainted_2 = null;
            string tainted_3 = null;

                            tainted_2 = var_4250;
                            
                string pattern = "^[\\.\\.\\/]+";
                Regex r = new Regex(pattern);
                tainted_3 = r.Replace(tainted_2, "");
            
                            return tainted_3;
                        }
                        
                    }
                }
