        <?php
        /*
        input : Uses popen to read the file /tmp/tainted.txt using cat command
Uses a magic_quotes_filter via filter_var function
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
        
        $tainted_1 = null;
        $tainted_2 = null;
        $tainted_3 = null;

        $handle = popen('/bin/cat /tmp/tainted.txt', 'r');
$tainted_1 = fread($handle, 4096);
pclose($handle);
        
                $arr_1 = array(); // declaring array
                //Storing value in array element
                $arr_1[] = null;
                $arr_1[] = null;
                $arr_1[] = null;
                $arr_1[] = $tainted_1;
                foreach($arr_1 as $val_1){
                    if($val_1!=null){
                        $tainted_2 = $val_1;
                        $sanitized = filter_var($tainted_2, FILTER_SANITIZE_ADD_SLASHES);
          $tainted_3 = $sanitized ;
      
                    }
                }
        
        
        $query = sprintf("SELECT * FROM student where id=%d", $tainted_3);
    
        
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
