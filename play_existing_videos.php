<!DOCTYPE html>
<html lang="en">
<head>
<link rel="stylesheet" type="text/css" href="programming_project_2.css">
	<title>Member-Login</title>
</head>
<body>
<script language="javascript" type="text/javascript">
	function popup() {
		window.location = 'testing.php?run=test';
	}
</script>
<div style="text-align: center;">
	<h1><strong>Congrats, you've successfully uploaded videos!</strong></h1>
	<h3><strong>Videos currently on your folders:</strong></h3>
	<?php
	

	$dir    = 'outputvids/';
	$video_files = [];

	foreach(glob($dir.'/*.*') as $file) {
	    $file_parts = pathinfo($file);
	    if ($file_parts['extension'] == "mp4"){
	        $video_files[] = $file;
	    }
	}

	foreach($video_files as $video_file) {
		$videoname = explode("/",$video_file);
		echo "<form action=\"\" method=\"POST\">";
	    echo "<video width=\"450\" height=\"400\" autoplay controls>";
	    echo "<source src='http://localhost/". $video_file ."' type='video/mp4'>";
	    echo "</video>";
	}
	echo "<br/>";
	?>
</div>
</body>
</html>