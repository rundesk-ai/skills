<?php

declare(strict_types=1);

namespace App;

use PDO;

final class Database
{
    public static function connect(string $dsn = 'sqlite:' . __DIR__ . '/../billing.sqlite'): PDO
    {
        $db = new PDO($dsn);
        $db->exec('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password_hash TEXT, roles TEXT)');
        $db->exec('CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, customer TEXT, total_cents INTEGER)');
        return $db;
    }
}
