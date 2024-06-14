        <?php
        /*
        input : execute a ls command using the function system, and put the last result in $tainted
Flushes content of $sanitized if the filter email_filter is not applied
construction : use of sprintf via a %d with simple quote
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
        
        $tainted_2 = null;
        $tainted_3 = null;
        $tainted_4 = null;

        $tainted_2 = system('ls', $retval);
        
                if (filter_var($tainted_2, FILTER_VALIDATE_EMAIL))
      $tainted_3 = $tainted_2 ;
    else
      $tainted_3 = "" ;
                $tainted_4 = function_1($tainted_3);
        
        
        $query = sprintf("SELECT * FROM student where id='%d'", $tainted_4);
    
        
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
                    return $param_1 ;
                }


        ?>
