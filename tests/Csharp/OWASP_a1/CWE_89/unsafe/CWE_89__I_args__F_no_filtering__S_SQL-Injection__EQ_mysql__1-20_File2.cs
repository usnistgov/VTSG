
                /*
                Command line args
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
                    class Class_29603{
                        string var_29603;
                        public Class_29603(string tainted_2_29603){
                            var_29603 = tainted_2_29603;
                        }
                        public string get_var_29603(){
                            string tainted_2 = null;
            string tainted_3 = null;

                            tainted_2 = var_29603;
                            
                //No filtering (sanitization)
                tainted_3 = tainted_2;
            
                            return tainted_3;
                        }
                        
                    }
                }
