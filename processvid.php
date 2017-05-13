<?php
function processvid($name) {
	shell_exec('bash cgi-bin/videosplit ' . $name);
}
?>