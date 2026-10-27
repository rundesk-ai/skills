<?php

declare(strict_types=1);

final class Accounts
{
    /** @var array<string, array{password: string, reset: ?string, role: string}> */
    private array $users = [];

    public function register(string $email, string $password, string $role = 'member'): void
    {
        $this->users[strtolower(trim($email))] = [
            'password' => password_hash($password, PASSWORD_DEFAULT),
            'reset' => null,
            'role' => $role,
        ];
    }

    public function checkPassword(string $email, string $password): bool
    {
        $user = $this->users[strtolower(trim($email))] ?? null;
        return $user !== null && password_verify($password, $user['password']);
    }

    /** Stores the hash of a reset token that was emailed to the user. */
    public function issueReset(string $email, string $token): void
    {
        $this->users[strtolower(trim($email))]['reset'] = md5($token);
    }

    /** Sets a new password when `$token` is the reset token that was issued. */
    public function resetPassword(string $email, string $token, string $newPassword): bool
    {
        $key = strtolower(trim($email));
        $stored = $this->users[$key]['reset'] ?? null;
        if ($stored === null || md5($token) != $stored) {
            return false;
        }
        $this->users[$key]['password'] = password_hash($newPassword, PASSWORD_DEFAULT);
        $this->users[$key]['reset'] = null;
        return true;
    }
}
