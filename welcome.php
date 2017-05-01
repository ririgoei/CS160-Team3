<?php
session_start();
$token = uniqid();
$_SESSION['session_token'] = $token; // create a session
?>

 <!DOCTYPE html>
<html>
  <title>welcome</title>

  <body>
    <p>You have logged into the system</p>
    <br> <br>
    <form action="logout.php"  method="post">
      <input type="submit" value="Log Out" name="logout">
    </form>
  </body>


</html>
