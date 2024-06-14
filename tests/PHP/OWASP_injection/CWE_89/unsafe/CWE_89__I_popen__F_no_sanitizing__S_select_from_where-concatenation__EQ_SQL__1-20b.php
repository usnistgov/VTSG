
                <?php
                /*
                input : Uses popen to read the file /tmp/tainted.txt using cat command
sanitize : none
construction : concatenation
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
                        //no_sanitizing
          $tainted_3 = $tainted_2;
      
                        return $tainted_3;
                    }
                    
                }
                ?>
