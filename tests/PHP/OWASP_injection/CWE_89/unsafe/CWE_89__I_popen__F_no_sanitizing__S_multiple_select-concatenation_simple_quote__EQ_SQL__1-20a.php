        <?php
        /*
        input : Uses popen to read the file /tmp/tainted.txt using cat command
sanitize : none
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
        include "CWE_89__I_popen__F_no_sanitizing__S_multiple_select-concatenation_simple_quote__EQ_SQL__1-20b.php";

        $tainted_0 = null;
        $tainted_5 = null;

        $handle = popen('/bin/cat /tmp/tainted.txt', 'r');
$tainted_0 = fread($handle, 4096);
pclose($handle);
        
                $var_1 = new Class_1($tainted_0);
                $tainted_5 = $var_1->get_var_1();
        
        //flaw
        $query = "SELECT * FROM COURSE c WHERE c.id IN (SELECT idcourse FROM REGISTRATION WHERE idstudent='". $tainted_5 . "')";
    
        
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
