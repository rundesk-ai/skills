<?php

declare(strict_types=1);

use App\Auth;
use App\Database;
use App\Invoice;
use App\Reports;
use App\Subscription;

function test_invoice_total(): void
{
    $invoice = new Invoice(1, 'acme', [
        ['sku' => 'a-1', 'qty' => 2, 'price_cents' => 1250],
        ['sku' => 'b-2', 'qty' => 1, 'price_cents' => 999],
    ]);
    assert_same(3499, $invoice->totalCents());
}

function test_export_uppercases_skus(): void
{
    $invoice = new Invoice(1, 'acme', [['sku' => ' a-1 ', 'qty' => 2, 'price_cents' => 1250]]);
    assert_same(['A-1,2,2500'], $invoice->exportRows());
}

function test_renewal_moves_one_month(): void
{
    $sub = new Subscription(new DateTime('2026-03-10'), new DateTime('2026-03-10'), 1900);
    assert_same('2026-04-10', $sub->renew()->format('Y-m-d'));
}

function test_renewal_from_month_end(): void
{
    $sub = new Subscription(new DateTime('2026-01-31'), new DateTime('2026-01-31'), 1900);
    assert_same('2026-03-03', $sub->renew()->format('Y-m-d'));
}

function test_due_date_is_fourteen_days_later(): void
{
    assert_same('2026-05-15', Subscription::dueDate(new DateTime('2026-05-01'))->format('Y-m-d'));
}

function test_login(): void
{
    $db = Database::connect('sqlite::memory:');
    Auth::register($db, 'pat@shop.example', 'correct horse');
    $auth = new Auth($db);
    assert_same('pat@shop.example', $auth->login('pat@shop.example', 'correct horse')['email'] ?? null);
    assert_same(null, $auth->login('pat@shop.example', 'wrong'));
}

function test_report_sorts_by_total(): void
{
    $db = Database::connect('sqlite::memory:');
    $db->exec("INSERT INTO invoices (customer, total_cents) VALUES ('b', 300), ('a', 100), ('c', 200)");
    $rows = (new Reports($db))->invoices('total_cents', 'desc');
    assert_same([300, 200, 100], array_map(fn ($r) => (int) $r['total_cents'], $rows));
}
