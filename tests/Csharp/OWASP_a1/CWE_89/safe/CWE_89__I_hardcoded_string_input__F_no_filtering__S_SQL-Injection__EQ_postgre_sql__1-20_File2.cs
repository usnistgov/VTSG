
                /*
                Hardcoded string input
no filtering
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
                
                namespace default_namespace{
                    class Class_29048{
                        string var_29048;
                        public Class_29048(string tainted_2_29048){
                            var_29048 = tainted_2_29048;
                        }
                        public string get_var_29048(){
                            string tainted_2 = null;
            string tainted_3 = null;

                            tainted_2 = var_29048;
                            
                //No filtering (sanitization)
                tainted_3 = tainted_2;
            
                            return tainted_3;
                        }
                        
                    }
                }
