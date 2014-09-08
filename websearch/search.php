<!DOCTYPE  HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"  "http://www.w3.org/TR/html4/loose.dtd"> 
<?php
  $host = "127.0.0.1";
  $schema = "logbot";
  $user = "i_can_read";
  $pass = "&just4Me";

  $db=mysql_connect  ($host, $user, $pass) or die ('DB Conn failed: ' . mysql_error());
  $mydb=mysql_select_db($schema);
  
  //ini_set('display_errors', 'On');
  //error_reporting(E_ALL);
?>  
<style type="text/css"><?php include './inc/stylesheet.css'; ?></style>
  <html> 
    <head> 
        <meta  http-equiv="Content-Type" content="text/html;  charset=iso-8859-1"> 
        <title>Archives Search</title> 
    </head> 
    <body> 
    <H1> All times in GMT0 </H1>

    <div class="searchTable">

    <table border="1">
        <tr>
        <td> Time </td>
        <td> Message </td>
        <td> User </td>
        <td> Channel </td>
        </tr>         
        
      <?php      
      if(isset($_POST['submitName'])){
        $search=$_POST['sName'];
      if(preg_match("/^[  a-zA-Z]+/", $_POST['submitName'])){
        $sql="SELECT * FROM tbl_archive WHERE message LIKE '%" . $search .  "%' OR user LIKE '%" . $search ."%'";
        }
      }
      if(isset($_POST['submitDate'])){
        $search=$_POST['sDate'];
      if(preg_match("/^[  a-zA-Z]+/", $_POST['submitDate'])){
        $sql="SELECT * FROM tbl_archive WHERE time LIKE '" . $search .  "%'";
        }
      }
      if(isset($_GET['go'])){
        $result=mysql_query($sql);
        while($row=mysql_fetch_array($result)){
          echo "<tr><td>".$row[0]."</td><td>".$row[1]."</td><td>".$row[2]."</td><td>".$row[3]."</td></tr>";
        }
      } else {
        echo "</table></div><br><br><h2>No Data</h2>";
      }
      ?>
        
      </table> 
    </div>
  </body>
</html>