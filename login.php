<?php
?>

<!DOCTYPE html>
<html>

  <title>Registration</title>

  <body>
    <form action="\cgi-bin\getUser2.cgi" method="post">
      User Name: <br />
      <input type="text" name="username" required />
      <br />
      Password: <br />
      <input type="password" name="password" required />
      <br /> <br />
      
      <input type="submit" value="Log In" />
    </form>
  </body>

</html>
