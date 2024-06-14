        <?php
        /*
        input : use exec to execute the script /tmp/tainted.sh and store the output in $tainted
Flushes content of $sanitized if the filter email_filter is not applied
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
        
        $tainted_1 = null;
        $tainted_2 = null;
        $tainted_3 = null;

        
        $script = "/tmp/tainted.sh";
        exec($script, $result, $return);
        $tainted_1 = $result[0];
        
                $arr_1 = array(); // declaring array
                //Storing value in array element
                $arr_1[] = null;
                $arr_1[] = null;
                $arr_1[] = null;
                $arr_1[] = $tainted_1;
                foreach($arr_1 as $val_1){
                    if($val_1!=null){
                        $tainted_2 = $val_1;
                        if (filter_var($tainted_2, FILTER_VALIDATE_EMAIL))
      $tainted_3 = $tainted_2 ;
    else
      $tainted_3 = "" ;
                    }
                }
        
        //flaw
        $query = "SELECT lastname, firstname FROM drivers, vehicles WHERE drivers.id = vehicles.ownerid AND vehicles.tag='". $tainted_3 . "'";
    
        
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
