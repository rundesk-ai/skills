<?php

namespace App\Policies;

use App\Enums\OrderStatus;
use App\Models\Order;
use App\Models\User;

class OrderPolicy
{
    public function view(User $user, Order $order): bool
    {
        return $user->id === $order->user_id || $user->is_admin;
    }

    /**
     * Only an order still pending may be cancelled, by its customer or an admin.
     */
    public function cancel(User $user, Order $order): bool
    {
        return $order->status === OrderStatus::Pending
            && ($user->id === $order->user_id || $user->is_admin);
    }
}
