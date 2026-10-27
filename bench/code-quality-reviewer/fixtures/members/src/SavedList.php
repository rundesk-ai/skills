<?php

declare(strict_types=1);

final class SavedList
{
    /** @var list<string> */
    private array $items = [];

    public function add(string $item): void
    {
        if (!in_array($item, $this->items, true)) {
            $this->items[] = $item;
        }
    }

    /** Removes `$item`; returns false when it was not in the list. */
    public function remove(string $item): bool
    {
        $pos = array_search($item, $this->items, true);
        if (!$pos) {
            return false;
        }
        array_splice($this->items, $pos, 1);
        return true;
    }

    /** @return list<string> */
    public function items(): array
    {
        return $this->items;
    }
}
