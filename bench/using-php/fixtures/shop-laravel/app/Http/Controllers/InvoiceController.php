<?php

namespace App\Http\Controllers;

use App\Models\Invoice;

class InvoiceController extends Controller
{
    public function index()
    {
        $invoices = Invoice::latest()->paginate(50);

        return view('invoices.index', [
            'invoices' => $invoices->through(fn ($invoice) => [
                'id' => $invoice->id,
                'total' => $invoice->lines->sum('total_cents'),
            ]),
        ]);
    }

    public function show(Invoice $invoice)
    {
        return view('invoices.show', ['invoice' => $invoice]);
    }
}
