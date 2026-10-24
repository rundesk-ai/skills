<?php

declare(strict_types=1);

namespace App;

use PDO;

final class Auth
{
    public function __construct(private PDO $db)
    {
    }

    /** @return array{id: int, email: string, roles: list<string>}|null */
    public function login(string $email, string $password): ?array
    {
        $stmt = $this->db->prepare('SELECT id, email, password_hash, roles FROM users WHERE email = ?');
        $stmt->execute([$email]);
        $user = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($user && md5($password) == $user['password_hash']) {
            return [
                'id' => (int) $user['id'],
                'email' => $user['email'],
                'roles' => explode(',', $user['roles']),
            ];
        }
        return null;
    }

    public static function register(PDO $db, string $email, string $password, string $roles = 'customer'): void
    {
        $db->prepare('INSERT INTO users (email, password_hash, roles) VALUES (?, ?, ?)')
            ->execute([$email, md5($password), $roles]);
    }
}
