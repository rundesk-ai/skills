<?php

declare(strict_types=1);

final class Publishing
{
    private const PUBLISHERS = ['admin', 'editor'];

    /** Whether the request's user may publish. `$request` is the decoded JSON body. */
    public static function canPublish(array $request): bool
    {
        return in_array($request['role'] ?? null, self::PUBLISHERS);
    }

    /** Escapes a title for HTML, quotes included. */
    public static function titleHtml(string $title): string
    {
        return htmlspecialchars($title, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
    }
}
