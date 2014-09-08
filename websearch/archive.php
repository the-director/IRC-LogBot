<!DOCTYPE  HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"  "http://www.w3.org/TR/html4/loose.dtd"> 
<?php
  //ini_set('display_errors', 'On');
  //error_reporting(E_ALL);
?>
<html> 
    <head> 
        <meta  http-equiv="Content-Type" content="text/html;  charset=iso-8859-1"> 
            <title>Archives Search</title> 
    </head> 
    <body> 
        <h3>Search Archives</h3> 
        <p>Please enter Search Criteria:</p> 
        Username or text in message:
        <form  method="post" action="search.php?go"  id="searchform"> 
            <input  type="text" name="sName"> 
            <input  type="submit" name="submitName" value="Search by text">
            <br>
            <br>
            Date:
            <br>
            <form  method="post" action="search.php?go"  id="searchform"> 
            <input  type="date" name="sDate"> 
            <input  type="submit" name="submitDate" value="Search by date"> 
        </form>
        </form> 
    </body> 
</html> 