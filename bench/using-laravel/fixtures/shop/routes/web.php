<?php

use App\Http\Controllers\OrderController;
use App\Http\Controllers\OrdersExportController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

Route::middleware('auth')->group(function () {
    Route::get('/orders', [OrderController::class, 'index'])->name('orders.index');
    Route::post('/orders', [OrderController::class, 'store'])->name('orders.store');
    Route::get('/orders/export', [OrdersExportController::class, 'csv'])->name('orders.export');
    Route::get('/orders/{order}', [OrderController::class, 'show'])->name('orders.show');
    Route::post('/orders/{order}/cancel', [OrderController::class, 'cancel'])->name('orders.cancel');

    Route::middleware('can:admin')->prefix('admin')->name('admin.')->group(function () {
        Route::view('/', 'admin.index')->name('index');
    });
});
