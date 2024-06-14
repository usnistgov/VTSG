
                <?php
                /*
                input : use fopen to read /tmp/tainted.txt and put the first line in $tainted
sanitize : use of the function htmlentities. Sanitizes the query but has a high chance to produce unexpected results
construction : interpretation
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
                    function __construct($param){
                        $this->var_1 = $param;
                    }
                    function get_var_1(){
                        return $this->var_1;
                    }
                }
                ?>
