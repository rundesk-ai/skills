<?php

declare(strict_types=1);

// A dependency-free test runner: every function in tests/*Test.php whose name starts with test_ runs.
require __DIR__ . '/bootstrap.php';

function assert_same(mixed $expected, mixed $actual, string $message = ''): void
{
    if ($expected !== $actual) {
        throw new RuntimeException(sprintf("%s\nexpected: %s\n  actual: %s", $message, var_export($expected, true), var_export($actual, true)));
    }
}

foreach (glob(__DIR__ . '/*Test.php') as $file) {
    require $file;
}

$failed = 0;
$ran = 0;
foreach (get_defined_functions()['user'] as $fn) {
    if (!str_starts_with($fn, 'test_')) {
        continue;
    }
    $ran++;
    try {
        $fn();
        echo "ok   $fn\n";
    } catch (Throwable $e) {
        $failed++;
        echo "FAIL $fn\n  " . str_replace("\n", "\n  ", $e->getMessage()) . "\n";
    }
}
echo "\n$ran tests, $failed failed\n";
exit($failed > 0 ? 1 : 0);
