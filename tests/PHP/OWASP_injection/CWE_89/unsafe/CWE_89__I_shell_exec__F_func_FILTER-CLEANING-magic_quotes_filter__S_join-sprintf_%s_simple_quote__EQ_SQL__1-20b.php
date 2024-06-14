
                <?php
                /*
                input : use shell_exec to cat /tmp/tainted.txt
Uses a magic_quotes_filter via filter_var function
construction : use of sprintf via a %s with simple quote
SQL Query
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
                
                class Class_1{
                    var $var_1;
                    function __construct($tainted_2_1){
                        $this->var_1 = $tainted_2_1;
                    }
                    function get_var_1(){
                        $tainted_2 = null;
        $tainted_3 = null;

                        $tainted_2 = $this->var_1;
                        $sanitized = filter_var($tainted_2, FILTER_SANITIZE_ADD_SLASHES);
          $tainted_3 = $sanitized ;
      
                        return $tainted_3;
                    }
                    
                }
                ?>
