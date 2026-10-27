+++
subject = "code-quality-reviewer"
kind = "quality"
difficulty = "complex"
trap = "security holes behind checks that look right, beside correct versions of the same patterns"
fixture = "auth"
cases_version = 2
key = """
must:
  M1 bug+rule  redirect.safeNext accepts any string starting with "/", so "//evil.example/x" (a protocol-relative URL) passes and resolves to https://evil.example/x (reproduced): an open redirect after sign-in, the classic phishing step. Breaks "redirect only to paths on this site". Fix: use sameSiteUrl, or require "/" not followed by "/" or "\\".
  M2 bug       jwt.verify returns the payload whenever the token's own header says alg "none", so an unsigned token for any subject is accepted (reproduced: {"sub":"admin"} with no signature). Fix: require header.alg === "HS256" and always check the signature.
  M3 bug+rule  jwt.verify never checks exp, so a token signed 30 days ago still verifies (reproduced). Breaks "A session token expires 24 hours after sign-in". Fix: refuse when payload.exp is missing or not in the future.
  M4 bug+rule  settings.mergeSettings recursively merges the parsed request body, and JSON.parse keeps "__proto__" as an own key, so {"__proto__": {"isAdmin": true}} writes onto Object.prototype; after one request every user, including a new {}, passes canManageShop (reproduced). Breaks "Every request input is untrusted". Fix: skip "__proto__", "constructor" and "prototype", or merge into Object.create(null), or validate the body against the known settings keys.
good code:
  G1 redirect.sameSiteUrl: resolves against the site and compares origins; correct.
  G2 apikey.keyMatches: length check then crypto.timingSafeEqual; correct and constant-time.
  G3 the signature comparison inside jwt.verify uses timingSafeEqual with a length check; correct (the bugs are the alg and exp handling, not the comparison).
decoys:
  D1 validate.STAFF_EMAIL looks like a ReDoS candidate but is unambiguous (each dot between alphanumerics) and runs in linear time; flagging it as catastrophic backtracking is a false positive.
  D2 verify returning null for malformed base64 or JSON is correct.
taste:
  T1 Buffer.from(head, 'base64url') passed straight to JSON.parse; T2 no JSDoc; T3 the `b64` helper name.
extras:
  X1 sign does not let the caller set a shorter lifetime.
  X2 verify does not check typ.
  X3 safeNext does not reject a backslash form ("/\\evil.example"), which some browsers normalise to "//"; same root cause as M1.
"""
+++
Review the `src` directory of this repository for code quality: bugs, AGENTS.md violations, and improvements worth fixing.
