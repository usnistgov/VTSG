        <?php
        /*
        input : get the UserData field of $_SESSION
Flushes content of $sanitized if the filter number_float_filter is not applied
construction : concatenation with simple quote
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
        
        $tainted_0 = null;
        $tainted_5 = null;

        $tainted_0 = $_SESSION['UserData'];
        $tainted_5 = function_1($tainted_0);
        
        
        $query = "SELECT lastname, firstname FROM drivers, vehicles WHERE drivers.id = vehicles.ownerid AND vehicles.tag='". $tainted_5 . "'";
    
        
            $conn = mysql_connect('localhost', 'mysql_user', 'mysql_password'); // Connection to the database (address, user, password)
            mysql_select_db('dbname') ;
            echo "query : ". $query ."<br /><br />" ;

            $res = mysql_query($query); //execution

            while($data =mysql_fetch_array($res)){
            print_r($data) ;
            echo "<br />" ;
            }
            mysql_close($conn);
        
        
                function function_1(string $param_1 ){
                    $tainted_2 = null;
        $tainted_3 = null;

                    $tainted_2 = $param_1;
                    if (filter_var($tainted_2, FILTER_VALIDATE_FLOAT))
      $tainted_3 = $tainted_2 ;
    else
      $tainted_3 = "" ;
    
                    return $tainted_3;
                }
        ?>
