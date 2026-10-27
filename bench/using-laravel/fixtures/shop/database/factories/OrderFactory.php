<?php

namespace Database\Factories;

use App\Enums\OrderStatus;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<\App\Models\Order>
 */
class OrderFactory extends Factory
{
    public function definition(): array
    {
        return [
            'user_id' => User::factory(),
            'reference' => 'ORD-'.fake()->unique()->numerify('#####'),
            'status' => OrderStatus::Pending,
            'total_cents' => fake()->numberBetween(1_000, 100_000),
            'due_at' => now()->addDays(14),
        ];
    }

    public function overdue(): static
    {
        return $this->state(['due_at' => now()->subDays(3)]);
    }

    public function paid(): static
    {
        return $this->state(['status' => OrderStatus::Paid]);
    }
}
