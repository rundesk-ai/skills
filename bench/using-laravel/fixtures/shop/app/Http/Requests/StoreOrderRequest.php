<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreOrderRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'reference' => ['required', 'string', 'max:40', 'unique:orders,reference'],
            'total_cents' => ['required', 'integer', 'min:1'],
            'due_at' => ['required', 'date', 'after:today'],
        ];
    }
}
