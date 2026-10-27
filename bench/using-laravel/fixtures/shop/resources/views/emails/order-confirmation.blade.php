<p>{{ __('orders.confirmation_greeting', ['name' => $order->user->name]) }}</p>

<p>{{ __('orders.confirmation_body', ['reference' => $order->reference]) }}</p>

<p>{{ __('orders.total') }}: {{ Number::currency($order->total_cents / 100, 'EUR') }}</p>

<p>{{ __('orders.due') }}: {{ $order->due_at->toFormattedDateString() }}</p>
