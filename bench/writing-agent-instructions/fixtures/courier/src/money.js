// Fees are integers in the currency's minor unit (cents, pence). No float ever holds money.
export function addFees(...minor) {
  for (const m of minor) if (!Number.isInteger(m)) throw new TypeError("fee must be an integer minor unit");
  return minor.reduce((a, b) => a + b, 0);
}

export function format(minor, currency) {
  return `${(minor / 100).toFixed(2)} ${currency}`;
}
