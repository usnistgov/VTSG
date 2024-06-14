        <?php
        /*
        input : backticks interpretation, reading the file /tmp/tainted.txt
Uses a number_int_filter via filter_var function
construction : interpretation
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

        $tainted_2 = `cat /tmp/tainted.txt`;
        
                do{
                    $sanitized = filter_var($tainted_2, FILTER_SANITIZE_NUMBER_INT);
    if (filter_var($sanitized, FILTER_VALIDATE_INT))
      $tainted_3 = $sanitized ;
    else
      $tainted_3 = "" ;
    
                    break;
                }while((1==1));
        
        
        $query = "SELECT * FROM COURSE c WHERE c.id IN (SELECT idcourse FROM REGISTRATION WHERE idstudent= $tainted_3 )";
    
        
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
