        <?php
        /*
        input : use fopen to read /tmp/tainted.txt and put the first line in $tainted
Uses a full_special_chars_filter via filter_var function
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
        $tainted_1 = null;

        $handle = @fopen("/tmp/tainted.txt", "r");

if ($handle) {
  if(($tainted_0 = fgets($handle, 4096)) == false) {
    $tainted_0 = "";
  }
  fclose($handle);
} else {
  $tainted_0 = "";
}
        $sanitized = filter_var($tainted_0, FILTER_SANITIZE_FULL_SPECIAL_CHARS);
          $tainted_1 = $sanitized ;
     
        
        
        $query = sprintf("SELECT * FROM student where id=%d", $tainted_1);
    
        
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
