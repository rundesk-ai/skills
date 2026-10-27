// Staff accounts must use the shop's own domain. Each dot must sit between letters or digits, so
// the pattern has one way to match any input and runs in linear time.
const STAFF_EMAIL = /^[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*@shop\.example$/;

export function isStaffEmail(email) {
  return STAFF_EMAIL.test(email);
}
