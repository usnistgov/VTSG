        <?php
        /*
        input : use fopen to read /tmp/tainted.txt and put the first line in $tainted
Flushes content of $sanitized if the filter number_float_filter is not applied
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
        
        $tainted_2 = null;
        $tainted_3 = null;

        $handle = @fopen("/tmp/tainted.txt", "r");

if ($handle) {
  if(($tainted_2 = fgets($handle, 4096)) == false) {
    $tainted_2 = "";
  }
  fclose($handle);
} else {
  $tainted_2 = "";
}
        
                for($i_1 = 0; $i_1 <= 1; $i_1++){
                    if (filter_var($tainted_2, FILTER_VALIDATE_FLOAT))
      $tainted_3 = $tainted_2 ;
    else
      $tainted_3 = "" ;
    
                }
        
        
        $query = "SELECT * FROM '". $tainted_3 . "'";
    
        
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
