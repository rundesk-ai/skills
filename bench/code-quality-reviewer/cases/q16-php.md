+++
subject = "code-quality-reviewer"
kind = "quality"
difficulty = "complex"
trap = "PHP loose comparison traps beside correct strict code in the same files"
fixture = "members"
cases_version = 2
key = """
declare(strict_types=1) is on in every file; it governs argument types, not == or in_array, so it does not prevent any of these.
must:
  M1 bug+rule  Accounts.resetPassword compares md5 hashes with !=; two hashes of the form "0e" plus digits compare as the number 0, so a different token resets the password when the issued token's hash is one (md5("240610708") matches md5("QNKCDZO"), reproduced). md5 is also a fast unsalted hash for a secret. Breaks "accepted only when it is exactly the one that was issued". Fix: hash_equals($stored, hash('sha256', $token)), or store a password_hash of the token.
  M2 bug+rule  Publishing.canPublish uses in_array without strict mode on a value from decoded JSON; {"role": true} matches any non-empty string, so it may publish (reproduced). Breaks "Only admin and editor may publish". Fix: in_array(..., true) and require a string role.
  M3 bug       SavedList.remove treats array_search's result with !$pos, so an item at position 0 is reported as not found and never removed (reproduced: removing "tea", the first item, returns false). The tests only remove the second item. Fix: if ($pos === false).
good code:
  G1 Accounts.checkPassword: password_verify against password_hash; correct.
  G2 SavedList.add uses in_array(..., true); correct, unlike M2.
  G3 Publishing.titleHtml: htmlspecialchars with ENT_QUOTES | ENT_SUBSTITUTE and UTF-8; correct.
decoys:
  D1 $user !== null and $stored === null are strict and correct.
  D2 strtolower(trim($email)) is applied the same way in every method: consistent.
taste:
  T1 final classes; T2 static method on Publishing; T3 array shapes in docblocks rather than value objects.
extras:
  X1 issueReset on an unknown email creates a partial user record with only a reset key.
  X2 reset tokens never expire.
"""
+++
Review this PHP project for code quality: bugs, AGENTS.md violations, and improvements worth fixing.
