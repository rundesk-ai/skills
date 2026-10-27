<?php

declare(strict_types=1);

require __DIR__ . '/../src/Accounts.php';
require __DIR__ . '/../src/Publishing.php';
require __DIR__ . '/../src/SavedList.php';

$failures = 0;
function check(string $name, bool $ok): void
{
    global $failures;
    echo ($ok ? 'ok   ' : 'FAIL ') . $name . PHP_EOL;
    $failures += $ok ? 0 : 1;
}

$a = new Accounts();
$a->register('Ada@example.com', 'correct horse battery');
check('password checks', $a->checkPassword('ada@example.com', 'correct horse battery') && !$a->checkPassword('ada@example.com', 'nope'));
$a->issueReset('ada@example.com', 'f3a9c2d1e8b7');
check('wrong reset token refused', !$a->resetPassword('ada@example.com', 'wrong-token', 'x'));
check('right reset token accepted', $a->resetPassword('ada@example.com', 'f3a9c2d1e8b7', 'new password here'));
check('new password works', $a->checkPassword('ada@example.com', 'new password here'));

check('editor may publish', Publishing::canPublish(['role' => 'editor']));
check('member may not publish', !Publishing::canPublish(['role' => 'member']));
check('title escaped', Publishing::titleHtml('<b>"Hi"</b>') === '&lt;b&gt;&quot;Hi&quot;&lt;/b&gt;');

$l = new SavedList();
$l->add('tea');
$l->add('cake');
$l->add('cake');
check('no duplicates', $l->items() === ['tea', 'cake']);
check('remove second', $l->remove('cake') && $l->items() === ['tea']);
check('remove missing', !$l->remove('scones'));

echo $failures === 0 ? "all passed\n" : "$failures failed\n";
exit($failures === 0 ? 0 : 1);
