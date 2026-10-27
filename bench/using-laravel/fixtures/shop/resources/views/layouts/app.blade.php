<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <title>@yield('title', config('app.name'))</title>
</head>
<body>
    <main>
        @yield('content')
    </main>
</body>
</html>
