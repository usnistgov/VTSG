        <?php
        /*
        input : Get a serialize string in POST and unserialize it
sanitize : use of ternary condition
construction : use of sprintf via a %u
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
        include "CWE_89__I_unserialize__F_ternary_white_list_order_direction__S_select_from_where-sprintf_%u__EQ_SQL__1-22b.php";

        $tainted_2 = null;
        $tainted_3 = null;
        $tainted_4 = null;

        $string = $_POST['UserData'] ;
        $tainted_2 = unserialize($string);
    
        
                $tainted_3 = $tainted_2  == 'DESC' ? 'DESC' : 'ASC';
                $var_1 = new Class_1($tainted_3);
                $tainted_4 = $var_1->get_var_1();
        
        
        $query = sprintf("SELECT * FROM student where id=%u", $tainted_4);
    
        
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
