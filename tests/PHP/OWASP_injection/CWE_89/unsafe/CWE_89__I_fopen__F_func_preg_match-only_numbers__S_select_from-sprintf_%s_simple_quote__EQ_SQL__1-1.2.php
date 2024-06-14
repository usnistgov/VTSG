        <?php
        /*
        input : use fopen to read /tmp/tainted.txt and put the first line in $tainted
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
        $tainted_3 = $tainted_2;
        
                if((1==0)){
                    $re = "/^[0-9]*$/";
        if(preg_match($re, $tainted_2) == 1){
          $tainted_3 = $tainted_2;
        }
        else{
          $tainted_3 = "";
        }
                }
        
        //flaw
        $query = sprintf("SELECT * FROM '%s'", $tainted_3);
    
        
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
