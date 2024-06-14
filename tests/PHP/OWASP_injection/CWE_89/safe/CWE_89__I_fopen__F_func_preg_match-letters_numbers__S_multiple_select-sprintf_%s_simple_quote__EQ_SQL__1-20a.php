        <?php
        /*
        input : use fopen to read /tmp/tainted.txt and put the first line in $tainted
sanitize : check if there is only letters and/or numbers
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
        include "CWE_89__I_fopen__F_func_preg_match-letters_numbers__S_multiple_select-sprintf_%s_simple_quote__EQ_SQL__1-20b.php";

        $tainted_0 = null;
        $tainted_5 = null;

        $handle = @fopen("/tmp/tainted.txt", "r");

if ($handle) {
  if(($tainted_0 = fgets($handle, 4096)) == false) {
    $tainted_0 = "";
  }
  fclose($handle);
} else {
  $tainted_0 = "";
}
        
                $var_1 = new Class_1($tainted_0);
                $tainted_5 = $var_1->get_var_1();
        
        
        $query = sprintf("SELECT * FROM COURSE c WHERE c.id IN (SELECT idcourse FROM REGISTRATION WHERE idstudent='%s')", $tainted_5);
    
        
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
