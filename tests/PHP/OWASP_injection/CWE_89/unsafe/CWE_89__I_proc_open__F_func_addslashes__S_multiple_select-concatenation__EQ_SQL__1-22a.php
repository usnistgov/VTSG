        <?php
        /*
        input : use proc_open to read /tmp/tainted.txt
sanitize : use of the function addslashes
construction : concatenation
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
        include "CWE_89__I_proc_open__F_func_addslashes__S_multiple_select-concatenation__EQ_SQL__1-22b.php";

        $tainted_2 = null;
        $tainted_3 = null;
        $tainted_4 = null;

        $descriptorspec = array(
  0 => array("pipe", "r"),
  1 => array("pipe", "w"),
  2 => array("file", "/tmp/error-output.txt", "a")
  );
$cwd = '/tmp';
$process = proc_open('more /tmp/tainted.txt', $descriptorspec, $pipes, $cwd, NULL);
if (is_resource($process)) {
  fclose($pipes[0]);
  $tainted_2 = stream_get_contents($pipes[1]);
  fclose($pipes[1]);
  $return_value = proc_close($process);
}
        
                $tainted_3 = addslashes($tainted_2);
                $var_1 = new Class_1($tainted_3);
                $tainted_4 = $var_1->get_var_1();
        
        //flaw
        $query = "SELECT * FROM COURSE c WHERE c.id IN (SELECT idcourse FROM REGISTRATION WHERE idstudent=". $tainted_4 . ")";
    
        
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
