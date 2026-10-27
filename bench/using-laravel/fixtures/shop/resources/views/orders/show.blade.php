@extends('layouts.app')

@section('title', $order->reference)

@section('content')
    <h1>{{ $order->reference }}</h1>

    <dl>
        <dt>{{ __('orders.status') }}</dt>
        <dd>{{ $order->status->value }}</dd>
        <dt>{{ __('orders.total') }}</dt>
        <dd>{{ Number::currency($order->total_with_vat_cents / 100, 'EUR') }}</dd>
        <dt>{{ __('orders.due') }}</dt>
        <dd>{{ $order->due_at->toFormattedDateString() }}</dd>
    </dl>

    @can('cancel', $order)
        <form method="POST" action="{{ route('orders.cancel', $order) }}">
            @csrf
            <button>{{ __('orders.cancel') }}</button>
        </form>
    @endcan
@endsection
