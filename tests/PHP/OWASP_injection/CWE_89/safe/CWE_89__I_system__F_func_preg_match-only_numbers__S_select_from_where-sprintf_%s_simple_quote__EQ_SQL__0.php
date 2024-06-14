        <?php
        /*
        input : execute a ls command using the function system, and put the last result in $tainted
sanitize : check if there is only numbers
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
        
        $tainted_0 = null;
        $tainted_1 = null;

        $tainted_0 = system('ls', $retval);
        $re = "/^[0-9]*$/";
        if(preg_match($re, $tainted_0) == 1){
          $tainted_1 = $tainted_0;
        }
        else{
          $tainted_1 = "";
        }
        
        
        $query = sprintf("SELECT * FROM student where id='%s'", $tainted_1);
    
        
            $conn = mysql_connect('localhost', 'mysql_user', 'mysql_password'); // Connection to the database (address, user, password)
            mysql_select_db('dbname') ;
            echo "query : ". $query ."<br /><br />" ;

            $res = mysql_query($query); //execution

            while($data =mysql_fetch_array($res)){
            print_r($data) ;
            echo "<br />" ;
            }
            mysql_close($conn);
        
        
        ?>
