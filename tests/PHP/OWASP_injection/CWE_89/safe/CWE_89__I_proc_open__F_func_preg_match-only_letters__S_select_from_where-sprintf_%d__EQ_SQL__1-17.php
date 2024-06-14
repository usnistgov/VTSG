        <?php
        /*
        input : use proc_open to read /tmp/tainted.txt
sanitize : check if there is only letters
construction : use of sprintf via a %d
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

        $descriptorspec = array(
  0 => array("pipe", "r"),
  1 => array("pipe", "w"),
  2 => array("file", "/tmp/error-output.txt", "a")
  );
$cwd = '/tmp';
$process = proc_open('more /tmp/tainted.txt', $descriptorspec, $pipes, $cwd, NULL);
if (is_resource($process)) {
  fclose($pipes[0]);
  $tainted_0 = stream_get_contents($pipes[1]);
  fclose($pipes[1]);
  $return_value = proc_close($process);
}
        $tainted_5 = function_1($tainted_0);
        
        
        $query = sprintf("SELECT * FROM student where id=%d", $tainted_5);
    
        
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
                    
        $re = "/^[a-zA-Z]*$/";
        if(preg_match($re, $tainted_2) == 1){
          $tainted_3 = $tainted_2;
        }
        else{
          $tainted_3 = "";
        }
        
                    return $tainted_3;
                }
        ?>
