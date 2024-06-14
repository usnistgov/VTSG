        <?php
        /*
        input : use exec to execute the script /tmp/tainted.sh and store the output in $tainted
sanitize : use of the function htmlentities. Sanitizes the query but has a high chance to produce unexpected results
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

        
        $script = "/tmp/tainted.sh";
        exec($script, $result, $return);
        $tainted_2 = $result[0];
        
                do{
                    $tainted_3 = htmlentities($tainted_2, ENT_QUOTES);
                    break;
                }while((1==1));
        
        //flaw
        $query = sprintf("SELECT lastname, firstname FROM drivers, vehicles WHERE drivers.id = vehicles.ownerid AND vehicles.tag='%s'", $tainted_3);
    
        
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
