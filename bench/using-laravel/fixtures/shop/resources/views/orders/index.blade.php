@extends('layouts.app')

@section('title', __('orders.title'))

@section('content')
    <h1>{{ __('orders.title') }}</h1>

    @include('orders.partials.export-button')

    <table>
        <thead>
            <tr>
                <th>{{ __('orders.reference') }}</th>
                <th>{{ __('orders.status') }}</th>
                <th>{{ __('orders.total') }}</th>
                <th></th>
            </tr>
        </thead>
        <tbody>
            @foreach ($orders as $order)
                <tr>
                    <td><a href="{{ route('orders.show', $order) }}">{{ $order->reference }}</a></td>
                    <td>{{ $order->status->value }}</td>
                    <td>{{ Number::currency($order->total_with_vat_cents / 100, 'EUR') }}</td>
                    <td>
                        @can('cancel', $order)
                            <form method="POST" action="{{ route('orders.cancel', $order) }}">
                                @csrf
                                <button>{{ __('orders.cancel') }}</button>
                            </form>
                        @endcan
                    </td>
                </tr>
            @endforeach
        </tbody>
    </table>

    {{ $orders->links() }}
@endsection
