
                /*
                input : shell commands
filtering : check if there is only numbers
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
                using System.Text.RegularExpressions;
                namespace default_namespace{
                    class Class_31268{
                        string var_31268;
                        public Class_31268(string tainted_2_31268){
                            var_31268 = tainted_2_31268;
                        }
                        public string get_var_31268(){
                            string tainted_2 = null;
            string tainted_3 = null;

                            tainted_2 = var_31268;
                            
                string pattern = @"/^[0-9]*$/";
                Regex r = new Regex(pattern);
                Match m = r.Match(tainted_2);
                if(!m.Success){
                    tainted_3 = "";
                }else{
                    tainted_3 = tainted_2;
                }
            
                            return tainted_3;
                        }
                        
                    }
                }
