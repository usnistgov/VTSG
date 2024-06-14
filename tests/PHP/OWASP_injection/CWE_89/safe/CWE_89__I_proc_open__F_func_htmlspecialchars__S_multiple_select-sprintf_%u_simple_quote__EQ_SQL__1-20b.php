
                <?php
                /*
                input : use proc_open to read /tmp/tainted.txt
sanitize : use of the function htmlspecialchars. Sanitizes the query but has a high chance to produce unexpected results
construction : use of sprintf via a %u with simple quote
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
                        $tainted_3 = htmlspecialchars($tainted_2, ENT_QUOTES);
                        return $tainted_3;
                    }
                    
                }
                ?>
