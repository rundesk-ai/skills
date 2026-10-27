<?php

return [

    /*
    | VAT added to every order total, in basis points (2,100 is 21%).
    */
    'vat_bp' => (int) env('BILLING_VAT_BP', 2100),

];
