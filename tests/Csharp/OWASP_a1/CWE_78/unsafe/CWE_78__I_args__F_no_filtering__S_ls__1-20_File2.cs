
                /*
                Command line args
no filtering
sink : run ls in a dir
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
                    class Class_23675{
                        string var_23675;
                        public Class_23675(string tainted_2_23675){
                            var_23675 = tainted_2_23675;
                        }
                        public string get_var_23675(){
                            string tainted_2 = null;
            string tainted_3 = null;

                            tainted_2 = var_23675;
                            
                //No filtering (sanitization)
                tainted_3 = tainted_2;
            
                            return tainted_3;
                        }
                        
                    }
                }
