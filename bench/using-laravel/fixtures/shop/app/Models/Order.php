<?php

namespace App\Models;

use App\Enums\OrderStatus;
use Database\Factories\OrderFactory;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Fillable(['user_id', 'reference', 'status', 'total_cents', 'due_at'])]
class Order extends Model
{
    /** @use HasFactory<OrderFactory> */
    use HasFactory;

    protected function casts(): array
    {
        return [
            'status' => OrderStatus::class,
            'due_at' => 'datetime',
        ];
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * Orders still unpaid after their due date.
     */
    #[Scope]
    protected function overdue(Builder $query): void
    {
        $query->where('status', OrderStatus::Pending)->where('due_at', '<', now());
    }

    /**
     * The order total with VAT added, in cents, rounded down to the cent.
     */
    protected function totalWithVatCents(): Attribute
    {
        return Attribute::make(
            get: fn () => intdiv($this->total_cents * (10_000 + config('billing.vat_bp')), 10_000),
        );
    }
}
