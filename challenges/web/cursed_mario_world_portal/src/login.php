<?php
require('config.php');
session_start();

function validate($parsed, $admin_email, $admin_password) {

    if (isset($parsed['email']) && isset($parsed['password'])) {
        if ($parsed['email'] !== $admin_email || $parsed['password'] !== $admin_password) {
            http_response_code(401); // Unauthorized
			echo "Bad credentials\n";
            return;
        }
    }
    
	$_SESSION['isAuthenticated'] = true;
	http_response_code(200); // OK
    echo "Success\n";
	return;
}

if ($_SERVER['REQUEST_METHOD'] == 'GET') {
	if (isset($_GET['source'])) {
		highlight_file(__FILE__);
		die();
	}
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $json_input = file_get_contents('php://input');
    $parsed = json_decode($json_input, true);

    if (json_last_error() !== JSON_ERROR_NONE) {
        http_response_code(400); // Bad Request
        echo "Invalid JSON\n";
    } elseif (strpos($json_input, 'email') === false || strpos($json_input, 'password') === false) {
        http_response_code(400); // Bad Request
        echo "Missing input\n";
    } else {
        validate($parsed, $admin_email, $admin_password);
    }
}
?>
