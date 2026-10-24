<?php

declare(strict_types=1);

namespace App;

use DateTime;

final class Subscription
{
    public function __construct(
        public DateTime $startedAt,
        public DateTime $paidThrough,
        public int $priceCents,
    ) {
    }

    /** Extend the paid period by one month and return the new renewal date. */
    public function renew(): DateTime
    {
        $next = $this->paidThrough;
        $next->modify('+1 month');
        $this->paidThrough = $next;
        return $next;
    }

    /** Invoices are due fourteen days after they are issued. */
    public static function dueDate(DateTime $issuedAt): DateTime
    {
        return $issuedAt->modify('+14 days');
    }
}
