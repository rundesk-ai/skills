<?php

declare(strict_types=1);

namespace App;

use PDO;

final class Reports
{
    public function __construct(private PDO $db)
    {
    }

    /** Invoices for the admin report, sorted by a column the user picks in the table header. */
    public function invoices(string $sort = 'id', string $direction = 'asc'): array
    {
        $sql = "SELECT id, customer, total_cents FROM invoices ORDER BY $sort $direction";
        return $this->db->query($sql)->fetchAll(PDO::FETCH_ASSOC);
    }

    public function byCustomer(string $customer): array
    {
        $stmt = $this->db->prepare('SELECT id, customer, total_cents FROM invoices WHERE customer = ?');
        $stmt->execute([$customer]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
}
