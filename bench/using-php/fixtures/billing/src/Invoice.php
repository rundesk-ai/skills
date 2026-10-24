<?php

declare(strict_types=1);

namespace App;

final class Invoice
{
    /** @param list<array{sku: string, qty: int, price_cents: int}> $lines */
    public function __construct(
        public int $id,
        public string $customer,
        public array $lines,
    ) {
    }

    public function totalCents(): int
    {
        $total = 0;
        foreach ($this->lines as $line) {
            $total += $line['qty'] * $line['price_cents'];
        }
        return $total;
    }

    /** CSV rows for the accounting export: SKU, quantity, line total. */
    public function exportRows(): array
    {
        foreach ($this->lines as &$line) {
            $line['sku'] = strtoupper(trim($line['sku']));
        }

        $rows = [];
        foreach ($this->lines as $line) {
            $rows[] = $line['sku'] . ',' . $line['qty'] . ',' . $line['qty'] * $line['price_cents'];
        }
        return $rows;
    }
}
