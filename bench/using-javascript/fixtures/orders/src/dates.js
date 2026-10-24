// Invoice dates are stored as 'YYYY-MM-DD'.
export function dueDate(invoiceDate, termDays) {
  const date = new Date(invoiceDate);
  date.setDate(date.getDate() + termDays);
  return date;
}

export function formatDate(date) {
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${date.getFullYear()}-${month}-${day}`;
}
