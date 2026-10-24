# Orders

The order service: a Node HTTP server (`src/server.js`) and the helpers it uses. No framework and no
dependencies.

- Test: `npm test` (runs `node --test` in UTC, like CI).
- Start: `npm start`, then the service listens on port 3000.
- Invoice dates are calendar dates (`YYYY-MM-DD`) in the customer's own time zone.
- Warehouse order ids are 64-bit integers.
