        <?php
        /*
        input : Uses popen to read the file /tmp/tainted.txt using cat command
Uses a special_chars_filter via filter_var function
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
        include "CWE_89__I_popen__F_func_FILTER-CLEANING-special_chars_filter__S_multiple_select-interpretation__EQ_SQL__1-21b.php";

        $tainted_1 = null;
        $tainted_2 = null;
        $tainted_3 = null;

        $handle = popen('/bin/cat /tmp/tainted.txt', 'r');
$tainted_1 = fread($handle, 4096);
pclose($handle);
        
                $var_1 = new Class_1($tainted_1);
                $tainted_2 = $var_1->get_var_1();
                $sanitized = filter_var($tainted_2, FILTER_SANITIZE_SPECIAL_CHARS);
          $tainted_3 = $sanitized ;
      
        
        //flaw
        $query = "SELECT * FROM COURSE c WHERE c.id IN (SELECT idcourse FROM REGISTRATION WHERE idstudent= $tainted_3 )";
    
        
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
