#!/usr/bin/env node
// Sum the "amount" column of a CSV file: `csvtotal orders.csv`.
import { readFileSync } from 'node:fs';

export function total(csv) {
  const [header, ...rows] = csv.trim().split('\n');
  const col = header.split(',').indexOf('amount');
  return rows.reduce((sum, row) => sum + row.split(',')[col], 0);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  console.log(total(readFileSync(process.argv[2], 'utf8')));
}
