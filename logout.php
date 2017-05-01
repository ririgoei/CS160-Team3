<?php
// delete a session
session_start();
unset($_SESSION);
//session_destroy();
header("Location: login.php"); // redirect to the login page
?>
