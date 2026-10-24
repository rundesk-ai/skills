export const DEFAULTS = { currency: 'USD', pageSize: 25, format: { dates: 'iso' } };

// Deep-merge a user's saved preferences over the defaults.
export function merge(target, source) {
  for (const key in source) {
    if (typeof source[key] === 'object' && source[key] !== null) {
      target[key] = merge(target[key] ?? {}, source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}

export function canExport(user) {
  return user.isAdmin === true;
}
