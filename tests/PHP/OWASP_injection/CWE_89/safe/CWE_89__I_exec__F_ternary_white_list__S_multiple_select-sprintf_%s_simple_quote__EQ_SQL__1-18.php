        <?php
        /*
        input : use exec to execute the script /tmp/tainted.sh and store the output in $tainted
sanitize : use of ternary condition
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
        
        $tainted_1 = null;
        $tainted_2 = null;
        $tainted_3 = null;

        
        $script = "/tmp/tainted.sh";
        exec($script, $result, $return);
        $tainted_1 = $result[0];
        
                $tainted_2 = function_1($tainted_1);
                $tainted_3 = $tainted_2  == 'safe1' ? 'safe1' : 'safe2';
        
        
        $query = sprintf("SELECT * FROM COURSE c WHERE c.id IN (SELECT idcourse FROM REGISTRATION WHERE idstudent='%s')", $tainted_3);
    
        
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
