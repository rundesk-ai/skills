import { createServer } from "node:http";
import { logRequest } from "./log.js";

createServer((req, res) => {
  logRequest({ method: req.method, path: req.url }, 404);
  res.writeHead(404).end("not found");
}).listen(process.env.PORT || 3000);
