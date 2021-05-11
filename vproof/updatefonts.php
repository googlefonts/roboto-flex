<?php
set_time_limit(60);

$start = microtime(true);

exec("./updatefonts.sh", $output, $err);

if ($err > 0) {
	header("HTTP/1.1 500 Internal Server Error");
	header("Content-type: text/plain; charset=utf-8");
	print implode("\n", $output);
} else {
	$end = microtime(true);
	header("Content-type: text/plain; charset=utf-8");
	print "Run time: " . round($end - $start, 2) . "s";
}
