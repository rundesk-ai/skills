<?php

namespace Tests\Feature;

use App\Enums\OrderStatus;
use App\Mail\OrderConfirmation;
use App\Models\Order;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Mail;
use Tests\TestCase;

class OrderTest extends TestCase
{
    use RefreshDatabase;

    public function test_a_customer_sees_their_orders_with_vat_added(): void
    {
        $user = User::factory()->create();
        Order::factory()->for($user)->create(['reference' => 'ORD-1', 'total_cents' => 10_000]);

        $this->actingAs($user)->get('/orders')
            ->assertOk()
            ->assertSee('ORD-1')
            ->assertSee('€121.00');
    }

    public function test_placing_an_order_sends_the_confirmation(): void
    {
        Mail::fake();
        $user = User::factory()->create();

        $this->actingAs($user)->post('/orders', [
            'reference' => 'ORD-9', 'total_cents' => 5_000, 'due_at' => now()->addWeek()->toDateString(),
        ])->assertRedirect();

        Mail::assertSent(OrderConfirmation::class);
        $this->assertSame(OrderStatus::Pending, Order::firstWhere('reference', 'ORD-9')->status);
    }

    public function test_a_customer_can_cancel_a_pending_order_but_not_a_paid_one(): void
    {
        $user = User::factory()->create();
        $pending = Order::factory()->for($user)->create();
        $paid = Order::factory()->for($user)->paid()->create();

        $this->actingAs($user)->post("/orders/{$pending->id}/cancel")->assertRedirect();
        $this->actingAs($user)->post("/orders/{$paid->id}/cancel")->assertForbidden();

        $this->assertSame(OrderStatus::Cancelled, $pending->fresh()->status);
    }

    public function test_another_customer_cannot_see_an_order(): void
    {
        $order = Order::factory()->create();

        $this->actingAs(User::factory()->create())->get("/orders/{$order->id}")->assertForbidden();
    }

    public function test_the_overdue_scope_finds_pending_orders_past_their_due_date(): void
    {
        $overdue = Order::factory()->overdue()->create();
        Order::factory()->create();
        Order::factory()->overdue()->paid()->create();

        $this->assertEquals([$overdue->id], Order::overdue()->pluck('id')->all());
    }

    public function test_the_csv_export_lists_the_customers_orders(): void
    {
        $user = User::factory()->create();
        Order::factory()->for($user)->create(['reference' => 'ORD-7', 'total_cents' => 10_000]);

        $response = $this->actingAs($user)->get('/orders/export');

        $response->assertOk();
        $this->assertStringContainsString('ORD-7,pending,12100', $response->streamedContent());
    }

    public function test_only_admins_reach_the_admin_pages(): void
    {
        $this->actingAs(User::factory()->create())->get('/admin')->assertForbidden();
        $this->actingAs(User::factory()->create(['is_admin' => true]))->get('/admin')->assertOk();
    }
}
