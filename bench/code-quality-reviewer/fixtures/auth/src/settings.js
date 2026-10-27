// Applies a settings patch from the request body onto the stored settings, nested objects included.
export function mergeSettings(target, patch) {
  for (const [k, v] of Object.entries(patch)) {
    if (v && typeof v === 'object' && !Array.isArray(v)) {
      if (!target[k] || typeof target[k] !== 'object') target[k] = {};
      mergeSettings(target[k], v);
    } else {
      target[k] = v;
    }
  }
  return target;
}

export function updateSettings(user, body) {
  user.settings = mergeSettings(user.settings ?? {}, JSON.parse(body));
  return user.settings;
}

export function canManageShop(user) {
  return user.isAdmin === true;
}
