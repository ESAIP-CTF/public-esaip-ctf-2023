<?php
require('config.php');
session_start();

if (!isset($_SESSION['isAuthenticated']) || !$_SESSION['isAuthenticated']) {
    header('Location: index.html');
    exit();
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Protected Page</title>
    <style>
        body {
            background-image: url('mario-cursed-welcome.jpg');
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            height: 100%;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            color: red;
            text-shadow: 2px 2px 5px black;
            font-family: 'Courier New', Courier, monospace;
            font-size: 2em;
        }
    </style>
	<script>
      function randomPosition() {
        const width = window.innerWidth - 100;
        const height = window.innerHeight - 100;
        const x = Math.random() * width;
        const y = Math.random() * height;
        return { x, y };
      }
    
      function animateFlag() {
        const flag = document.getElementById('flag');
        const duration = 500; // 1 second
      
        setInterval(() => {
          const position = randomPosition();
          flag.style.left = position.x + 'px';
          flag.style.top = position.y + 'px';
          flag.style.opacity = 1;
      
          setTimeout(() => {
            flag.style.opacity = 0;
          }, duration / 2);
        }, duration);
      }
      
      document.addEventListener('DOMContentLoaded', () => {
        animateFlag();
      });
    </script>
</head>
<body>
    <h1 id="flag" style="position: absolute; opacity: 0;"><?php echo $flag; ?></h1>
</body>
</html>
