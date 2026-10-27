# Duplication and Dead Code

Each pattern below is written one reasonable change at a time, often by a different agent each time,
and each one compiles, passes its tests and reads fine in its own file. The cost arrives when the
rule changes and only one copy is updated, or when the next agent extends code nothing uses.

## Find the existing home by convention, not by name

Laravel calls most code by convention or by string, so a search for the method name misses its
readers. Before writing a rule, search for its existing home this way; before deleting anything,
search for its readers this way.

| The code | Its readers appear as |
| --- | --- |
| Scope `active` (`#[Scope] active()` or legacy `scopeActive()`) | `->active(`, `::active(` |
| Accessor `totalWithVatCents()` returning `Attribute`, or legacy `getTotalWithVatCentsAttribute()` | `total_with_vat_cents` in PHP, Blade, `$appends`, API resources and front-end code |
| View `orders.show` | `view('orders.show'`, `@include('orders.show'`, `@extends`, `View::make`, `Route::view`, `Inertia::render('Orders/Show')` |
| Component `App\View\Components\StatusBadge` or `components/status-badge.blade.php` | `<x-status-badge` |
| Route name `orders.export` | `route('orders.export'`, `to_route(`, `->route(`, front-end route helpers |
| Controller action | `php artisan route:list` (an invokable controller has no method name to search) |
| Policy ability `cancel` | `@can('cancel'`, `->can('cancel'`, `authorize('cancel'`, `Gate::allows('cancel'`, `can:cancel,` middleware |
| Event, listener | `php artisan event:list` (a discovered listener is registered by nothing you can search for), `::dispatch(`, `event(new` |
| Job, notification, mailable | `::dispatch(`, `dispatch(new`, `Bus::chain`, `Bus::batch`, `->notify(new`, `Mail::to(`, the scheduler |
| Artisan command | its `$signature` in `routes/console.php`, the scheduler, `Artisan::call(`, deploy scripts and documented runbooks |
| Config key `billing.vat_bp` | `config('billing.vat_bp'`, `Config::get(` |
| Translation key | `__('`, `trans(`, `trans_choice(`, `@lang(`, front-end translation helpers |

## One rule, one home

Incorrect — the VAT rule re-derived in a view, a mailable and an export, each its own copy:
```blade
{{-- resources/views/orders/show.blade.php --}}
{{ number_format($order->total_cents * 1.21 / 100, 2) }}
```
```php
// app/Mail/OrderShipped.php and app/Exports/OrdersCsv.php
'total' => $this->order->total_cents * 121 / 100,
```

Correct — the model owns the rule, read through config, and every surface reads the accessor:
```php
protected function totalWithVatCents(): Attribute
{
    return Attribute::make(
        get: fn () => intdiv($this->total_cents * (10_000 + config('billing.vat_bp')), 10_000),
    );
}
```
```blade
{{ Number::currency($order->total_with_vat_cents / 100, 'EUR') }}
```

The copies above already disagree: the view rounds a float, the mailable truncates an integer. When
copies disagree, merging them is a behaviour change: decide which is right and prove it with a test.

A query constraint written out twice belongs in a local scope; see
[Use Local Scopes for Reusable Queries](eloquent.md). Search for the scope by its call form before
writing `->where('due_at', '<', now())->where('status', 'unpaid')` again.

## Authorization and status, written once

Incorrect — the ownership rule in a controller, a Blade condition and an API resource, and the status
as a bare string in each:
```php
if ($order->user_id !== $request->user()->id || $order->status !== 'pending') {
    abort(403);
}
```
```blade
@if (auth()->id() === $order->user_id && $order->status === 'pending')
    <button>Cancel</button>
@endif
```

Correct — a policy owns the rule, a backed enum owns the states, and every surface asks:
```php
// app/Policies/OrderPolicy.php
public function cancel(User $user, Order $order): bool
{
    return $user->id === $order->user_id && $order->status === OrderStatus::Pending;
}
```
```php
Gate::authorize('cancel', $order);
```
```blade
@can('cancel', $order) <button>Cancel</button> @endcan
```

## A list of cases, a classification, a copy of state

Incorrect — the set of open statuses restated as cases, and a badge colour and a label each classifying
the order on their own; the next status added is missed by both:
```php
if (in_array($order->status, [OrderStatus::Pending, OrderStatus::Paid])) { ... }
```
```blade
<span class="{{ $order->status === OrderStatus::Shipped ? 'green' : 'amber' }}">
    {{ $order->status === OrderStatus::Shipped || $order->status === OrderStatus::Delivered ? 'Done' : 'Open' }}
</span>
```

Correct — the enum owns the set and the classification; every surface asks it:
```php
enum OrderStatus: string
{
    // ...cases
    public function isOpen(): bool
    {
        return in_array($this, [self::Pending, self::Paid], true);
    }
}
```
```blade
<span class="{{ $order->status->isOpen() ? 'amber' : 'green' }}">{{ $order->status->isOpen() ? 'Open' : 'Done' }}</span>
```

Search for the cases (`OrderStatus::Pending,`), not for the method you would name. The same goes for
state: a Livewire or front-end component that keeps its own copy of a model's status and re-applies its
rules drifts from it; read the model's value instead.

## Validation, written once

Incorrect — the web and API controllers each carry their own rule array, and one gains a rule the
other never gets:
```php
$request->validate(['email' => 'required|email', 'qty' => 'required|integer|min:1']);
```

Correct — one Form Request, injected wherever the input arrives:
```php
public function store(StoreOrderRequest $request) { ... }
```

## Built ahead of its reader

Incorrect — data handed to a view that never shows it, an accessor appended to every serialization
for a screen that does not exist yet, an event with no listener:
```php
return view('orders.index', compact('orders', 'stats', 'regions')); // the template uses only $orders
protected $appends = ['shipping_estimate'];                          // nothing reads it
OrderArchived::dispatch($order);                                     // event:list shows no listener
```

Correct — each arrives in the change that reads it. A test that only exercises it is not a reader.

## The replaced path left behind

Incorrect — the queued export replaced the synchronous one, and the old path stays wired:
```php
Route::get('/orders/export', [OrdersExportController::class, 'csv'])->name('orders.export');
Route::post('/orders/exports', StartOrdersExport::class)->name('orders.exports.store');
```
The old controller, its route, its `orders.export-progress` view, its translation keys and its test
all remain, and the next agent extends the wrong one.

Correct — in the same change: the old route and controller method, the views, components, config and
translation keys only they used, and the tests that only covered them, until nothing new is unused.

## Not dead, even with no reader in the repository

- **Migrations.** Old migrations build every fresh database and roll it back; never delete one to
  tidy up. Change the schema with a new migration.
- **API resource fields, webhook payloads and database columns.** Their readers are outside the
  repository; ask the owner before removing one.
- **Artisan commands run by cron, by hand or by a deploy script**, and routes linked from outside the
  app (emails, other services).

## The tools see little of it

PHP reports no unused code, and Laravel calls most code by string or convention, so static analysis
cannot prove a controller, view, job or listener unused. `php artisan route:list`, `event:list` and
`schedule:list` show what is wired; the search table above finds the rest.
