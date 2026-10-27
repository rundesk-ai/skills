<?php

namespace App\Http\Controllers;

use App\Enums\OrderStatus;
use App\Http\Requests\StoreOrderRequest;
use App\Mail\OrderConfirmation;
use App\Models\Order;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Illuminate\Support\Facades\Mail;
use Illuminate\View\View;

class OrderController extends Controller
{
    public function index(Request $request): View
    {
        $orders = Order::whereBelongsTo($request->user())->latest()->paginate(20);

        return view('orders.index', ['orders' => $orders]);
    }

    public function show(Order $order): View
    {
        Gate::authorize('view', $order);

        return view('orders.show', ['order' => $order]);
    }

    public function store(StoreOrderRequest $request): RedirectResponse
    {
        $order = $request->user()->orders()->create([
            ...$request->validated(),
            'status' => OrderStatus::Pending,
        ]);

        Mail::to($request->user())->send(new OrderConfirmation($order));

        return to_route('orders.show', $order);
    }

    public function cancel(Order $order): RedirectResponse
    {
        Gate::authorize('cancel', $order);

        $order->update(['status' => OrderStatus::Cancelled]);

        return back();
    }
}
