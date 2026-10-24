<h1>Invoices</h1>
<table>
    <tr><th><a href="?page=report&sort=id">#</a></th><th><a href="?page=report&sort=customer">Customer</a></th><th><a href="?page=report&sort=total_cents">Total</a></th></tr>
    <?php foreach ($rows as $row): ?>
        <tr><td><?= (int) $row['id'] ?></td><td><?= htmlspecialchars($row['customer']) ?></td><td><?= number_format($row['total_cents'] / 100, 2) ?></td></tr>
    <?php endforeach ?>
</table>
