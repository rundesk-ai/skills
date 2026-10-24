<?php

declare(strict_types=1);

spl_autoload_register(function (string $class): void {
    if (str_starts_with($class, 'App\\')) {
        require __DIR__ . '/../src/' . str_replace('\\', '/', substr($class, 4)) . '.php';
    }
});
