<?php

declare(strict_types=1);

require __DIR__ . '/../tests/bootstrap.php';

use App\Auth;
use App\Database;
use App\Reports;

session_start();
$db = Database::connect();

// Remembered table preferences (page size, columns) survive across sessions.
$prefs = isset($_COOKIE['prefs']) ? unserialize(base64_decode($_COOKIE['prefs'])) : ['page_size' => 25];

if (($_POST['action'] ?? '') === 'login') {
    $user = (new Auth($db))->login((string) $_POST['email'], (string) $_POST['password']);
    if ($user !== null) {
        $_SESSION['user'] = $user;
    }
}

$page = $_GET['page'] ?? 'home';

if ($page === 'report') {
    if (!in_array('admin', $_SESSION['user']['roles'] ?? [], true)) {
        http_response_code(403);
        exit('Forbidden');
    }
    $rows = (new Reports($db))->invoices($_GET['sort'] ?? 'id', $_GET['dir'] ?? 'asc');
}

include __DIR__ . '/../templates/' . $page . '.php';
