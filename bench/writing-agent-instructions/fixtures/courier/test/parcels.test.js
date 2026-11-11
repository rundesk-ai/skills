import { test } from "node:test";
import assert from "node:assert/strict";
import { createParcel } from "../src/routes/parcels.js";

const store = () => ({ saved: [], nextId: () => 1, save(p) { this.saved.push(p); } });
const body = { recipientAddress: "1 Canal Street", baseFeeMinor: 450, surchargeMinor: 50, currency: "EUR" };

test("a dispatcher creates a parcel with the summed fee", () => {
  const res = createParcel({ user: { role: "dispatcher" }, body }, store());
  assert.equal(res.status, 201);
  assert.equal(res.body.feeMinor, 500);
});

test("a courier may not create a parcel", () => {
  assert.equal(createParcel({ user: { role: "courier" }, body }, store()).status, 403);
});

test("a float fee is refused", () => {
  assert.throws(() => createParcel({ user: { role: "admin" }, body: { ...body, baseFeeMinor: 4.5 } }, store()), TypeError);
});
