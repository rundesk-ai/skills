// Live prices pushed by the pricing service. In the app the pricing socket calls publish(); the store
// also re-broadcasts every second so late subscribers catch up.
let prices = {};
const listeners = new Set();

export const priceStore = {
  get: () => prices,
  publish(next) {
    prices = { ...prices, ...next };
    listeners.forEach((l) => l());
  },
  subscribe(listener) {
    listeners.add(listener);
    return () => listeners.delete(listener);
  },
};

setInterval(() => listeners.forEach((l) => l()), 1000).unref?.();
