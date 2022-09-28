
                /*
                Hardcoded string input
no filtering
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
                
                namespace default_namespace{
                    class Class_6840{
                        string var_6840;
                        public Class_6840(string tainted_2_6840){
                            var_6840 = tainted_2_6840;
                        }
                        public string get_var_6840(){
                            string tainted_2 = null;
            string tainted_3 = null;

                            tainted_2 = var_6840;
                            
                //No filtering (sanitization)
                tainted_3 = tainted_2;
            
                            return tainted_3;
                        }
                        
                    }
                }
