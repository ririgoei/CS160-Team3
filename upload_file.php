<?php

$destination_path = "vids/"; 
$target_path = "vids/";
$target_path = $target_path . basename( $_FILES['file']['name']); 

#echo "User=" .          $user . "<br />";

if(move_uploaded_file($_FILES['file']['tmp_name'], $target_path)) {
    $filename = explode(".mp4", $_FILES['file']['name']);
    echo $filename[0];
    echo "The file has been uploaded";
    try{
      shell_exec('bash cgi-bin/process_vid ' . $filename[0]);
      print "<script>window.location = \"http://localhost/play_existing_videos.php\";</script></body></html>";
    } catch (Exception $e) {
        echo 'Caught exception: ',  $e->getMessage(), "\n";
    }
} else{
    echo "There was an error uploading the file, please try again!";
}
?>