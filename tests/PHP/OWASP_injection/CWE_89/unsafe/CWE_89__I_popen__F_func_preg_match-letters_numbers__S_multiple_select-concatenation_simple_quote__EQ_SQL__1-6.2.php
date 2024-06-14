        <?php
        /*
        input : Uses popen to read the file /tmp/tainted.txt using cat command
sanitize : check if there is only letters and/or numbers
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

        $handle = popen('/bin/cat /tmp/tainted.txt', 'r');
$tainted_2 = fread($handle, 4096);
pclose($handle);
        $tainted_3 = $tainted_2;
        
                if((1==0)){
                    $re = "/^[a-zA-Z0-9]*$/";
        if(preg_match($re, $tainted_2) == 1){
          $tainted_3 = $tainted_2;
        }
        else{
          $tainted_3 = "";
        }
                }else if(!(1==0)){
                    {}
                }else{
                    {}
                }
        
        //flaw
        $query = "SELECT * FROM COURSE c WHERE c.id IN (SELECT idcourse FROM REGISTRATION WHERE idstudent='". $tainted_3 . "')";
    
        
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
