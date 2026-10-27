<?php

namespace App\Http\Controllers;

use App\Models\Order;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\StreamedResponse;

class OrdersExportController extends Controller
{
    /**
     * Streams the signed-in customer's orders as CSV, built while the request waits.
     */
    public function csv(Request $request): StreamedResponse
    {
        $orders = Order::whereBelongsTo($request->user())->orderBy('id')->get();

        return response()->streamDownload(function () use ($orders) {
            $out = fopen('php://output', 'w');
            fputcsv($out, ['reference', 'status', 'total_with_vat_cents', 'due_at']);
            foreach ($orders as $order) {
                fputcsv($out, [$order->reference, $order->status->value, $order->total_with_vat_cents, $order->due_at->toDateString()]);
            }
            fclose($out);
        }, 'orders.csv', ['Content-Type' => 'text/csv']);
    }
}
