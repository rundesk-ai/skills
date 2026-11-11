// The only authorisation in the service: a route names the role it needs, and this refuses others.
export function requireRole(role) {
  return (req) => {
    if (!req.user) return { status: 401, body: "sign in" };
    if (req.user.role !== role && req.user.role !== "admin") return { status: 403, body: "forbidden" };
    return null;
  };
}
