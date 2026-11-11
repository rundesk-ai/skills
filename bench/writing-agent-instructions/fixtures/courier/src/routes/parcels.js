import { requireRole } from "../auth/requireRole.js";
import { addFees } from "../money.js";

const dispatcherOnly = requireRole("dispatcher");

export function createParcel(req, store) {
  const refused = dispatcherOnly(req);
  if (refused) return refused;
  const { recipientAddress, baseFeeMinor, surchargeMinor = 0, currency } = req.body;
  if (!recipientAddress || !currency) return { status: 422, body: "recipientAddress and currency are required" };
  const parcel = { id: store.nextId(), recipientAddress, feeMinor: addFees(baseFeeMinor, surchargeMinor), currency };
  store.save(parcel);
  return { status: 201, body: parcel };
}
