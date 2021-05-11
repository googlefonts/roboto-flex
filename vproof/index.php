<?php
namespace TypeNetwork\VideoProof;
require_once(__DIR__ . "/videoproof.inc");

$videoproof = new VideoProof();
?>
<!DOCTYPE html>
<html lang="en" id="videoproof">
	<head>
		<meta charset="utf-8">
		<title>Video Proof</title>
		<meta name="viewport" content="initial-scale=1,shrink-to-fit=no">
		<link rel="stylesheet" href="https://www.typenetwork.com/assets_content/css/reset.css">
		<link rel="stylesheet" href="https://www.typenetwork.com/assets_content/css/adobe-blank.css">
		<link rel="stylesheet" href="https://www.typenetwork.com/assets_content/css/fonts-momentum-sans.css">
		<link rel="stylesheet" href="https://www.typenetwork.com/assets_content/css/style.css">
		<link rel="icon" type="image/png" href="./favicon-32x32.png" sizes="32x32">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
		<script src="./opentype.js/dist/opentype.min.js"></script>
		<script src="./spectrum/spectrum.js"></script>
		<link rel="stylesheet" href="./spectrum/spectrum.css">

		<script src="https://www.typenetwork.com/assets_content/js/functions.js"></script>

		<style id='videoproof-keyframes'></style>
		<style id='videoproof-moar-animation'></style>
		
		<link rel="stylesheet" href="videoproof.css">
		<link rel="stylesheet" href="form-controls.css">

		<script src="videoproof.js"></script>

		<?= $videoproof->pageHead(); ?>
	</head>
	<body>
		<div class="wrapper">
			<header class="header-global">
				<h1><a href="https://www.typenetwork.com/">Type Network</a></h1>
			</header>
		
			<nav class="nav-global">
				<a class="nav-global-reveal" href="#">Menu</a>
				<ul>
<!--
					<li><a class="nav-home-link" href="https://www.typenetwork.com/">Home</a></li>
					<li><a href="http://store.typenetwork.com">Fonts</a></li>
					<li><a href="https://www.typenetwork.com/news" >News</a></li>
					<li><a href="https://www.typenetwork.com/gallery" >Gallery</a></li>
-->
				</ul>
			</nav>
			
			<nav class="nav-user">
				<a class="nav-user-reveal" href="#">Menu</a>
				<ul>
<!--
					<li><a href="http://store.typenetwork.com/account/licenses" class="nav-user-account"></a></li>
					<li><a href="http://store.typenetwork.com/account/favorites" class="nav-user-favorites"></a></li>
					<li><a href="http://store.typenetwork.com/cart" class="nav-user-cart"></a></li>
-->
				</ul>
			</nav>
			
			<?= $videoproof->pageSidebar() ?>
			
			<div class="content-main">
				<a class="content-options-show-filters" href="#">Sidebar</a>
				<output id='aniparams'>This animation will eat your CPU alive (depending on browser), so it doesn’t auto-start. Ready? <span id='first-play'>▶️</span></output>
				
				<div id='the-proof'></div>

				<footer class="footer-global">
					<ul>
						<li><a href="//www.typenetwork.com/about">About Type Network</a></li>
						<li><a href="//www.typenetwork.com/about#subscribe">Subscribe to the Newsletter</a></li>
						<li><a href="//www.typenetwork.com/support">Help and Support</a></li>
					</ul>
					<p>&copy; Type Network <?= date("Y") ?>. All rights reserved.</p>
				</footer>
			</div> <!-- content-main -->
		</div> <!-- wrapper -->
	</body>
</html>
