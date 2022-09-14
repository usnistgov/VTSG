
                /*
                input : direct user input in string
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
                    class Class_27753{
                        string var_27753;
                        public Class_27753(string tainted_2_27753){
                            var_27753 = tainted_2_27753;
                        }
                        public string get_var_27753(){
                            string tainted_2 = null;
            string tainted_3 = null;

                            tainted_2 = var_27753;
                            
                //No filtering (sanitization)
                tainted_3 = tainted_2;
            
                            return tainted_3;
                        }
                        
                    }
                }
