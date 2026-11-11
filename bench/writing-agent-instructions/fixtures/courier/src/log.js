// Logs a request line. Never the body: bodies hold recipients' names and home addresses.
export function logRequest(req, status) {
  process.stderr.write(`${req.method} ${req.path} ${status}\n`);
}
