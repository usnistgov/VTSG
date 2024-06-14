        <?php
        /*
        input : use shell_exec to cat /tmp/tainted.txt
sanitize : use of settype_int
construction : interpretation with simple quote
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

        $tainted_2 = shell_exec('cat /tmp/tainted.txt');
        
                if((1==0)){
                    {}
                }else{
                    if (settype($tainted_2, "integer"))
      $tainted_3 = $tainted_2 ;
    else
      $tainted_3 = 0 ;
    
                }
        
        
        $query = "SELECT * FROM student where id=' $tainted_3 '";
    
        
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
