#!/usr/bin/env bash
# Tests for scripts/deploy.sh, scripts/check.sh and scripts/bench-status.sh.
#
#   tests/run.sh            run everything
#   tests/run.sh <pattern>  run cases whose name matches
#
# These are integration tests against a real filesystem, because the whole contract of
# both scripts is what they leave on disk. Each case builds its own catalog fixture and
# its own target directory under one temp root, so cases share nothing and may be run in
# any order.
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FILTER="${1:-}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

discovered=0; executed=0; passed=0; failed=0
CASE=""

# What a directory holds, as one value: the paths, and the contents of every file.
# Directories count, because a fault can be an empty directory holding no file at all.
# cksum is POSIX and behaves the same on Linux and macOS, where md5 and md5sum do not
# both exist — a hash command that is missing returns the same empty value for every
# input, and a comparison against it passes whatever changed.
command -v cksum >/dev/null || { echo "cksum is missing; every comparison would pass"; exit 1; }
fingerprint() { { find "$1" | sort; find "$1" -type f -exec cksum {} + | sort; } | cksum; }

fail() { echo "    FAIL: $*"; failed=$((failed + 1)); CASE_OK=0; }

assert() {           # assert <description> <condition...>
  local desc="$1"; shift
  if "$@"; then :; else fail "$desc"; fi
}
assert_eq() {        # assert_eq <description> <expected> <actual>
  if [ "$2" = "$3" ]; then :; else fail "$1 — expected [$2], got [$3]"; fi
}
assert_file()    { [ -f "$1" ] || fail "expected file: ${2:-$1}"; }
assert_no_file() { [ ! -e "$1" ] || fail "expected absent: ${2:-$1}"; }
assert_link()    { [ -L "$1" ] || fail "expected symlink: ${2:-$1}"; }

run_case() {
  local name="$1"
  discovered=$((discovered + 1))
  if [ -n "$FILTER" ] && [[ "$name" != *"$FILTER"* ]]; then return; fi
  executed=$((executed + 1))
  CASE="$name"; CASE_OK=1
  echo "  - $name"
  "case_$name"
  [ "$CASE_OK" -eq 1 ] && passed=$((passed + 1))
}

# --- fixtures ---------------------------------------------------------------
# A catalog of two small skills, so a case's expected values are visible in the
# case itself rather than buried in the real catalog.
make_catalog() {
  local c="$1"
  mkdir -p "$c/scripts" "$c/skills/core/alpha/references" "$c/skills/core/beta"
  cp "$ROOT/scripts/deploy.sh" "$ROOT/scripts/check.sh" "$ROOT/scripts/bench-status.sh" "$c/scripts/"
  printf -- '---\nname: alpha\ndescription: Use when the alpha case needs proving in a test fixture catalog.\n---\n\n# Alpha\n\nRead [Base](references/base.md) for the base case.\n' \
    > "$c/skills/core/alpha/SKILL.md"
  printf 'base reference\n' > "$c/skills/core/alpha/references/base.md"
  printf -- '---\nname: beta\ndescription: Use when the beta case needs proving in a test fixture catalog.\n---\n\n# Beta\n' \
    > "$c/skills/core/beta/SKILL.md"
  printf '{"schema": 1, "name": "fixture", "version": "1.0.0", "description": "Fixture catalog.", "skills": [{"name": "alpha", "path": "skills/core/alpha"}, {"name": "beta", "path": "skills/core/beta"}], "subagents": [{"name": "gamma", "path": "subagents/gamma.md"}]}\n' \
    > "$c/manifest.json"
  mkdir -p "$c/subagents"
  printf -- '---\nname: gamma\ndescription: Use when the gamma case needs a subagent in a test fixture catalog.\nclaude:\n  model: sonnet\n---\nYou review the gamma case.\n' \
    > "$c/subagents/gamma.md"
  printf 'core alpha beta\n' > "$c/skills/groups.txt"
  printf '# AGENTS\n\nfixture\n' > "$c/AGENTS.md"
  sed '1s/AGENTS/CLAUDE/' "$c/AGENTS.md" > "$c/CLAUDE.md"
}

make_variant() {     # make_variant <catalog> — alpha@narrow replaces SKILL.md and drops base.md
  local c="$1"
  mkdir -p "$c/skills/core/alpha/variants/narrow"
  printf -- '---\nname: alpha\ndescription: Use when the narrowed alpha case needs proving in a fixture.\n---\n\n# Alpha (narrow)\n' \
    > "$c/skills/core/alpha/variants/narrow/SKILL.md"
  printf 'references/base.md\n' > "$c/skills/core/alpha/variants/narrow/.remove"
}

new_target() { local d="$TMP/$CASE-target-$RANDOM"; mkdir -p "$d"; echo "$d"; }
new_catalog() { local d="$TMP/$CASE-catalog-$RANDOM"; make_catalog "$d"; echo "$d"; }

# --- deploy.sh --------------------------------------------------------------

case_links_claude_to_the_one_copy() {
  local c t; c="$(new_catalog)"; t="$(new_target)"
  "$c/scripts/deploy.sh" "$t" alpha >/dev/null
  assert_file "$t/.agents/skills/alpha/SKILL.md" ".agents holds the real directory, read by Codex and Grok"
  assert_link "$t/.claude/skills" ".claude/skills is a symlink"
  assert_eq ".claude points at .agents" "../.agents/skills" "$(readlink "$t/.claude/skills")"
  assert_file "$t/.claude/skills/alpha/SKILL.md" ".claude resolves to the skill"
  assert "no .codex or .grok link is made" test ! -e "$t/.codex" -a ! -e "$t/.grok"
}

case_pushes_an_exact_copy() {
  local c t; c="$(new_catalog)"; t="$(new_target)"
  "$c/scripts/deploy.sh" "$t" alpha >/dev/null
  assert "the pushed skill is byte-identical to the catalog" \
    diff -r "$c/skills/core/alpha" "$t/.agents/skills/alpha"
}

case_is_idempotent() {
  local c t before after; c="$(new_catalog)"; t="$(new_target)"
  "$c/scripts/deploy.sh" "$t" alpha beta >/dev/null
  before="$(fingerprint "$t")"
  "$c/scripts/deploy.sh" "$t" alpha beta >/dev/null
  after="$(fingerprint "$t")"
  assert_eq "a second identical push changes nothing" "$before" "$after"
}

case_clears_a_skill_before_replacing_it() {
  # The reason the script clears rather than merges: a reference dropped from the
  # catalog must not survive in the target, where nothing would ever report it.
  local c t; c="$(new_catalog)"; t="$(new_target)"
  "$c/scripts/deploy.sh" "$t" alpha >/dev/null
  printf 'stale\n' > "$t/.agents/skills/alpha/references/dropped-upstream.md"
  "$c/scripts/deploy.sh" "$t" alpha >/dev/null
  assert_no_file "$t/.agents/skills/alpha/references/dropped-upstream.md" \
    "a file the catalog does not have is removed"
  assert_file "$t/.agents/skills/alpha/references/base.md" "a file it does have survives"
}

case_leaves_unnamed_skills_alone() {
  local c t; c="$(new_catalog)"; t="$(new_target)"
  "$c/scripts/deploy.sh" "$t" alpha >/dev/null
  mkdir -p "$t/.agents/skills/project-own"
  printf -- '---\nname: project-own\n---\n' > "$t/.agents/skills/project-own/SKILL.md"
  "$c/scripts/deploy.sh" "$t" alpha >/dev/null
  assert_file "$t/.agents/skills/project-own/SKILL.md" "a skill the project owns is untouched"
  assert_no_file "$t/.agents/skills/beta" "a catalog skill not asked for is not added"
}

case_applies_a_variant_overlay() {
  local c t; c="$(new_catalog)"; make_variant "$c"; t="$(new_target)"
  "$c/scripts/deploy.sh" "$t" alpha@narrow >/dev/null
  assert "the variant replaces the base file" \
    grep -q "Alpha (narrow)" "$t/.agents/skills/alpha/SKILL.md"
  assert_no_file "$t/.agents/skills/alpha/references/base.md" \
    ".remove drops the base file the variant does not carry"
  assert_no_file "$t/.agents/skills/alpha/variants" "the variants directory is never pushed"
  assert_no_file "$t/.agents/skills/alpha/.remove" "the removal list is never pushed"
}

case_switching_off_a_variant_restores_the_base() {
  local c t; c="$(new_catalog)"; make_variant "$c"; t="$(new_target)"
  "$c/scripts/deploy.sh" "$t" alpha@narrow >/dev/null
  "$c/scripts/deploy.sh" "$t" alpha >/dev/null
  assert_file "$t/.agents/skills/alpha/references/base.md" \
    "the file the variant removed comes back"
  assert "the base wording is restored" \
    grep -q "^# Alpha$" "$t/.agents/skills/alpha/SKILL.md"
}

case_all_pushes_every_skill() {
  local c t; c="$(new_catalog)"; t="$(new_target)"
  "$c/scripts/deploy.sh" "$t" --all >/dev/null
  assert_eq "every catalog skill is present" "2" "$(ls "$t/.agents/skills" | wc -l | tr -d ' ')"
}

case_sync_refreshes_only_what_is_installed() {
  local c t; c="$(new_catalog)"; t="$(new_target)"
  "$c/scripts/deploy.sh" "$t" alpha >/dev/null
  mkdir -p "$t/.agents/skills/project-own"
  printf -- '---\nname: project-own\n---\n' > "$t/.agents/skills/project-own/SKILL.md"
  printf 'stale\n' > "$t/.agents/skills/alpha/references/dropped-upstream.md"
  "$c/scripts/deploy.sh" "$t" --sync >/dev/null
  assert_no_file "$t/.agents/skills/alpha/references/dropped-upstream.md" \
    "an installed skill is refreshed"
  assert_no_file "$t/.agents/skills/beta" "a skill never installed is not added"
  assert_file "$t/.agents/skills/project-own/SKILL.md" \
    "a skill the catalog does not have is left alone"
}

case_sync_says_so_when_nothing_is_installed() {
  local c t out; c="$(new_catalog)"; t="$(new_target)"
  out="$("$c/scripts/deploy.sh" "$t" --sync 2>&1)"
  assert_eq "it exits successfully" "0" "$?"
  assert "it says nothing is installed" grep -q "nothing from this catalog is installed" <<< "$out"
  assert_no_file "$t/.agents/skills/alpha" "it pushes nothing"
}

case_dry_run_writes_nothing() {
  local c t; c="$(new_catalog)"; t="$(new_target)"
  "$c/scripts/deploy.sh" "$t" alpha --dry-run >/dev/null
  assert_no_file "$t/.agents" "no directory is created"
  assert_no_file "$t/.claude" "no agent home is created"
}

case_refuses_a_missing_directory() {
  local c status; c="$(new_catalog)"
  "$c/scripts/deploy.sh" "$TMP/no-such-dir" alpha >/dev/null 2>&1
  status=$?
  assert_eq "it exits 2 for a directory that does not exist" "2" "$status"
}

case_refuses_a_git_checkout() {
  local c t status; c="$(new_catalog)"; t="$(new_target)"
  git -C "$t" init -q
  mkdir -p "$t/sub"
  "$c/scripts/deploy.sh" "$t/sub" alpha >/dev/null 2>&1
  status=$?
  assert_eq "it exits 2 inside a git checkout" "2" "$status"
  assert "it writes nothing there" test ! -e "$t/sub/.agents"
}

case_refuses_an_unknown_skill_and_variant() {
  local c t out; c="$(new_catalog)"; t="$(new_target)"
  out="$("$c/scripts/deploy.sh" "$t" no-such-skill 2>&1)"
  assert "it names the missing skill" grep -q "no such skill: no-such-skill" <<< "$out"
  assert_no_file "$t/.agents/skills/no-such-skill" "nothing is written for it"
  out="$("$c/scripts/deploy.sh" "$t" alpha@no-such-variant 2>&1)"
  assert "it names the missing variant" grep -q "no such variant" <<< "$out"
  assert_no_file "$t/.agents/skills/alpha" "nothing is written for it either"
}

case_will_not_clobber_a_populated_agent_home() {
  # A project that already keeps real skills in .claude/skills would otherwise lose
  # them the first time anything was pushed.
  local c t out; c="$(new_catalog)"; t="$(new_target)"
  mkdir -p "$t/.claude/skills/theirs"
  printf -- '---\nname: theirs\n---\n' > "$t/.claude/skills/theirs/SKILL.md"
  out="$("$c/scripts/deploy.sh" "$t" alpha 2>&1)"
  assert_file "$t/.claude/skills/theirs/SKILL.md" "their skill survives"
  assert "it explains why it left the directory alone" \
    grep -q "real directory with skills in it" <<< "$out"
  assert_file "$t/.agents/skills/alpha/SKILL.md" "the skill still lands in .agents"
}

case_list_names_every_skill() {
  local c out; c="$(new_catalog)"
  out="$("$c/scripts/deploy.sh" --list)"
  assert_eq "it lists both fixture skills" "alpha
beta" "$out"
}

# --- check.sh ---------------------------------------------------------------

case_check_passes_a_sound_catalog() {
  local c status; c="$(new_catalog)"
  "$c/scripts/check.sh" >/dev/null 2>&1; status=$?
  assert_eq "a sound catalog exits 0" "0" "$status"
}

# Each of these proves the check has teeth: introduce one fault, expect a non-zero
# exit and a message naming it. A check that cannot fail protects nothing.
check_rejects() {    # check_rejects <description> <expected message> <mutate fn>
  local desc="$1" expect="$2" mutate="$3"
  local c out status before after; c="$(new_catalog)"
  "$c/scripts/check.sh" >/dev/null 2>&1 \
    || fail "$desc — the fixture was already failing before the mutation"
  before="$(fingerprint "$c")"
  "$mutate" "$c"
  after="$(fingerprint "$c")"
  [ "$before" != "$after" ] || fail "$desc — the mutation changed nothing, so the case proves nothing"
  out="$("$c/scripts/check.sh" 2>&1)"; status=$?
  assert_eq "$desc exits 1" "1" "$status"
  assert "$desc is named in the output" grep -q "$expect" <<< "$out"
}

# Each mutation introduces exactly one fault into a sound fixture catalog.
mutate_yaml_mapping()     { sed -i.bak "s/^description: Use when/description: Use when this: a mapping, when/" "$1/skills/core/alpha/SKILL.md"; }
mutate_yaml_comment()     { sed -i.bak "s/^description: Use when/description: Use when this #comment cuts it, when/" "$1/skills/core/alpha/SKILL.md"; }
mutate_yaml_indicator()   { sed -i.bak "s/^description: Use when/description: [Use when/" "$1/skills/core/alpha/SKILL.md"; }
mutate_subagent_yaml()    { sed -i.bak "s/^description: Use when/description: Use when this: a mapping, when/" "$1/subagents/gamma.md"; rm "$1/subagents/gamma.md.bak"; }
mutate_hollow_directory() { mkdir -p "$1/skills/core/hollow"; }
mutate_name_mismatch()    { sed -i.bak "s/^name: alpha/name: wrong/" "$1/skills/core/alpha/SKILL.md"; }
mutate_stub_description() { sed -i.bak "s/^description: .*/description: short/" "$1/skills/core/alpha/SKILL.md"; }
mutate_group_prefix()     { sed -i.bak "s/^core .*/core beta/" "$1/skills/groups.txt"; }   # alpha no longer fits
mutate_unlisted_group()   { mkdir -p "$1/skills/extra"; mv "$1/skills/core/beta" "$1/skills/extra/beta"; sed -i.bak 's#skills/core/beta#skills/extra/beta#' "$1/manifest.json"; }
mutate_not_use_when()     { sed -i.bak "s/^description: Use when/description: Helps when/" "$1/skills/core/alpha/SKILL.md"; }
mutate_unlinked_reference() { printf 'orphan\n' > "$1/skills/core/alpha/references/orphan.md"; }
mutate_cut_sentence()     { printf '\nSend that part of the work to\n' >> "$1/skills/core/alpha/SKILL.md"; }
mutate_cross_reference()  { printf 'see `beta` for that\n' >> "$1/skills/core/alpha/SKILL.md"; }
mutate_absolute_path()    { printf 'read /Users/someone/notes.md\n' >> "$1/skills/core/alpha/SKILL.md"; }
mutate_rule_drift()       { printf 'drifted\n' >> "$1/CLAUDE.md"; }
mutate_ungrouped_skill()  { mkdir -p "$1/skills/loose"; printf -- '---\nname: loose\ndescription: Use when the loose case needs proving in a test fixture catalog.\n---\n' > "$1/skills/loose/SKILL.md"; }
mutate_duplicate_name()   { mkdir -p "$1/skills/other/alpha"; cp "$1/skills/core/alpha/SKILL.md" "$1/skills/other/alpha/SKILL.md"; }
mutate_credential()       { printf 'token: ghp_abcdefghijklmnopqrstuvwxyz0123\n' >> "$1/skills/core/alpha/references/base.md"; }
mutate_real_email()       { printf 'write to someone@company.com\n' >> "$1/skills/core/alpha/SKILL.md"; }
mutate_integration_tool() { printf 'call mcp__tracker__create_issue first
' >> "$1/skills/core/alpha/SKILL.md"; }
mutate_manifest_missing() { printf '{"schema": 1, "name": "fixture", "version": "1.0.0", "description": "Fixture catalog.", "skills": [{"name": "alpha", "path": "skills/core/alpha"}], "subagents": [{"name": "gamma", "path": "subagents/gamma.md"}]}
' > "$1/manifest.json"; }
mutate_manifest_extra()   { printf '{"schema": 1, "name": "fixture", "version": "1.0.0", "description": "Fixture catalog.", "skills": [{"name": "alpha", "path": "skills/core/alpha"}, {"name": "beta", "path": "skills/core/beta"}, {"name": "gone", "path": "skills/core/gone"}], "subagents": [{"name": "gamma", "path": "subagents/gamma.md"}]}
' > "$1/manifest.json"; }
mutate_manifest_version() { sed -i.bak 's/"1.0.0"/"v1"/' "$1/manifest.json"; }
mutate_subagent_name()    { sed -i.bak "s/^name: gamma/name: delta/" "$1/subagents/gamma.md"; rm "$1/subagents/gamma.md.bak"; }
mutate_subagent_unlisted() { cp "$1/subagents/gamma.md" "$1/subagents/delta.md"; sed -i.bak "s/^name: gamma/name: delta/" "$1/subagents/delta.md"; rm "$1/subagents/delta.md.bak"; }
mutate_subagent_names_skill() { printf 'Then hand it to alpha.\n' >> "$1/subagents/gamma.md"; }
mutate_bad_removal() {
  mkdir -p "$1/skills/core/alpha/variants/narrow"
  printf -- '---\nname: alpha\n---\n' > "$1/skills/core/alpha/variants/narrow/SKILL.md"
  printf 'references/never-existed.md\n' > "$1/skills/core/alpha/variants/narrow/.remove"
}

case_check_rejects_a_directory_without_skill_md() {
  check_rejects "a directory with no SKILL.md" "no SKILL.md" mutate_hollow_directory
}
case_check_rejects_a_name_mismatch() {
  check_rejects "frontmatter naming another directory" "expected" mutate_name_mismatch
}
case_check_rejects_a_stub_description() {
  check_rejects "a description too short to route on" "too short" mutate_stub_description
}
case_check_accepts_links_and_fences_written_other_ways() {
  local c out status; c="$(new_catalog)"
  printf -- '---\nname: alpha\ndescription: Use when the alpha case needs proving in a test fixture catalog.\n---\n\n# Alpha\n\nRead [Base](./references/base.md "the base case") first.\n\n~~~text\nSend that part of the work to\n~~~\n\n#### Notes\n' \
    > "$c/skills/core/alpha/SKILL.md"
  printf 'See [Deep][deep] for the rest.\n\n[deep]: <deep%%20dive.md>\n' > "$c/skills/core/alpha/references/base.md"
  printf 'deep\n' > "$c/skills/core/alpha/references/deep dive.md"
  out="$("$c/scripts/check.sh" 2>&1)"; status=$?
  assert_eq "a titled ./ link, a reference-style link reached through another reference, and a fenced cut line all pass" "0" "$status"
  [ "$status" -eq 0 ] || echo "$out" | grep '!!' >&2
}
case_check_rejects_a_name_without_its_group_prefix() {
  check_rejects "a name that does not start with its group's prefix" "a name in core starts with" mutate_group_prefix
}
case_check_rejects_an_unlisted_group() {
  check_rejects "a group folder groups.txt does not list" "is not listed in skills/groups.txt" mutate_unlisted_group
}
case_check_rejects_a_description_not_starting_use_when() {
  check_rejects "a description that does not open with Use when" "must start 'Use when'" mutate_not_use_when
}
case_check_rejects_an_unlinked_reference() {
  check_rejects "a reference nothing links to" "no link reaches it" mutate_unlinked_reference
}
case_check_rejects_a_sentence_cut_short() {
  check_rejects "a sentence ending on a dangling word" "sentence ends mid-way" mutate_cut_sentence
}
case_check_rejects_a_cross_skill_reference() {
  check_rejects "one skill naming another" "each skill stands alone" mutate_cross_reference
}
case_check_rejects_an_absolute_path() {
  check_rejects "an absolute path" "a skill runs anywhere" mutate_absolute_path
}
case_check_rejects_drifted_rule_files() {
  check_rejects "AGENTS.md and CLAUDE.md differing" "differ" mutate_rule_drift
}
case_check_rejects_a_variant_removing_a_missing_file() {
  check_rejects "a .remove naming a file the base lacks" "the base does not have" mutate_bad_removal
}

case_check_rejects_a_skill_outside_a_group() {
  check_rejects "a skill directly under skills/" "put it in a group" mutate_ungrouped_skill
}
case_check_rejects_a_name_in_two_groups() {
  check_rejects "one name in two groups" "unique across groups" mutate_duplicate_name
}
case_check_rejects_a_credential() {
  check_rejects "a credential in a reference" "looks like a credential" mutate_credential
}
case_check_rejects_a_real_email() {
  check_rejects "a real email address" "real email address" mutate_real_email
}
case_check_accepts_reserved_email_domains() {
  local c status; c="$(new_catalog)"
  printf 'write to support@example.com or privacy@shop.example, never to a URL like https://docs.example.com/class_@gdscript.html\n' >> "$c/skills/core/alpha/SKILL.md"
  "$c/scripts/check.sh" >/dev/null 2>&1; status=$?
  assert_eq "reserved domains and URL fragments pass" "0" "$status"
}
# Installers parse frontmatter as YAML and reject the whole package when one file fails, so every
# skill in every project stops syncing. These are the plain-scalar faults that did it in v1.3.0.
case_check_rejects_an_unquoted_colon_in_frontmatter() {
  check_rejects "an unquoted ': ' in a description" "nested mapping" mutate_yaml_mapping
}
case_check_rejects_an_unquoted_hash_in_frontmatter() {
  check_rejects "an unquoted ' #' in a description" "start of a comment" mutate_yaml_comment
}
case_check_rejects_a_leading_yaml_indicator() {
  check_rejects "a description starting with '['" "reads as syntax" mutate_yaml_indicator
}
case_check_rejects_an_unquoted_colon_in_a_subagent() {
  check_rejects "an unquoted ': ' in a subagent description" "nested mapping" mutate_subagent_yaml
}
case_check_accepts_a_quoted_colon_in_frontmatter() {
  local c status; c="$(new_catalog)"
  sed -i.bak "s/^description: Use when\(.*\)$/description: \"Use when this: quoted\1\"/" "$c/skills/core/alpha/SKILL.md"
  "$c/scripts/check.sh" >/dev/null 2>&1; status=$?
  assert_eq "a quoted description may hold ': '" "0" "$status"
}
case_check_rejects_an_integration_tool() {
  check_rejects "a skill naming an integration's tool" "needs no integration" mutate_integration_tool
}
case_check_rejects_a_subagent_name_mismatch() {
  check_rejects "a subagent naming another file" "expected 'gamma'" mutate_subagent_name
}
case_check_rejects_an_unlisted_subagent() {
  check_rejects "a subagent the manifest leaves out" "does not list the subagent" mutate_subagent_unlisted
}
case_check_rejects_a_subagent_naming_a_skill() {
  check_rejects "a subagent naming a skill" "a subagent stands alone" mutate_subagent_names_skill
}
case_check_rejects_a_manifest_missing_a_skill() {
  check_rejects "a manifest that leaves out a skill" "does not list the skill" mutate_manifest_missing
}
case_check_rejects_a_manifest_listing_a_missing_skill() {
  check_rejects "a manifest naming a skill not in the tree" "not a skill in the tree" mutate_manifest_extra
}
case_check_rejects_a_bad_manifest_version() {
  check_rejects "a manifest version that is not MAJOR.MINOR.PATCH" "MAJOR.MINOR.PATCH" mutate_manifest_version
}

# --- bench-status.sh --------------------------------------------------------

record_result() {    # record_result <catalog> <skill> <date> [hash] — a result file as a run writes it
  local hash="${4:-}"
  mkdir -p "$1/bench/results/$2"
  if [ -n "$hash" ]; then
    printf '{"date": "%s", "skill": "%s", "skill_hash": "%s", "score": 0.5}\n' "$3" "$2" "$hash"
  else
    printf '{"date": "%s", "skill": "%s", "score": 0.5}\n' "$3" "$2"
  fi > "$1/bench/results/$2/$3.json"
}
bench_status() {     # bench_status <catalog> <args...> — prints "<status> <exit code>" for the first skill
  local c="$1" out status; shift
  out="$("$c/scripts/bench-status.sh" "$@")"; status=$?
  echo "$(echo "$out" | awk 'NR == 1 { print $2 }') $status"
}
fixture_git() { git -C "$1" -c user.name=test -c user.email=test@example.com "${@:2}" >/dev/null 2>&1; }

case_bench_status_reports_a_skill_never_run() {
  local c; c="$(new_catalog)"
  assert_eq "no result means a run is due" "never 1" "$(bench_status "$c" alpha)"
}
case_bench_status_skips_a_recent_unchanged_result() {
  local c; c="$(new_catalog)"
  record_result "$c" alpha "$(date +%F)" "$("$c/scripts/bench-status.sh" --hash alpha)"
  assert_eq "a result measuring what is there now is current" "current 0" "$(bench_status "$c" alpha)"
}
case_bench_status_reruns_a_changed_skill() {
  local c; c="$(new_catalog)"
  record_result "$c" alpha "$(date +%F)" "$("$c/scripts/bench-status.sh" --hash alpha)"
  printf 'one more rule\n' >> "$c/skills/core/alpha/SKILL.md"
  assert_eq "an edited skill is due" "changed 1" "$(bench_status "$c" alpha)"
}
case_bench_status_reruns_changed_cases() {
  local c; c="$(new_catalog)"
  record_result "$c" alpha "$(date +%F)" "$("$c/scripts/bench-status.sh" --hash alpha)"
  mkdir -p "$c/bench/alpha/cases" && printf 'a new case\n' > "$c/bench/alpha/cases/q09.md"
  assert_eq "a new case makes the skill due" "changed 1" "$(bench_status "$c" alpha)"
}
case_bench_status_reruns_an_old_result() {
  local c; c="$(new_catalog)"
  record_result "$c" alpha 2020-01-01 "$("$c/scripts/bench-status.sh" --hash alpha)"
  assert_eq "an unchanged result past the age limit is due" "old 1" "$(bench_status "$c" alpha)"
  assert_eq "--max-age moves the limit" "current 0" "$(bench_status "$c" --max-age 100000 alpha)"
}
case_bench_status_ignores_a_group_move() {
  local c; c="$(new_catalog)"
  record_result "$c" alpha "$(date +%F)" "$("$c/scripts/bench-status.sh" --hash alpha)"
  mkdir -p "$c/skills/other" && mv "$c/skills/core/alpha" "$c/skills/other/alpha"
  assert_eq "moving a skill between groups is not a change" "current 0" "$(bench_status "$c" alpha)"
}
case_bench_status_ignores_bytecode() {
  local c; c="$(new_catalog)"
  record_result "$c" alpha "$(date +%F)" "$("$c/scripts/bench-status.sh" --hash alpha)"
  mkdir -p "$c/bench/alpha/fixtures/app/__pycache__" && printf 'x' > "$c/bench/alpha/fixtures/app/__pycache__/m.pyc"
  assert_eq "bytecode a test run leaves is not a change" "current 0" "$(bench_status "$c" alpha)"
}
case_bench_status_compares_an_unhashed_result_with_its_commit() {
  # Results written before skill_hash existed: the commit that added the result is what it measured.
  local c; c="$(new_catalog)"
  record_result "$c" alpha "$(date +%F)"
  fixture_git "$c" init -q && fixture_git "$c" add -A && fixture_git "$c" commit -qm measured
  assert_eq "unchanged since the result's commit" "current 0" "$(bench_status "$c" alpha)"
  mkdir -p "$c/skills/other" && fixture_git "$c" mv skills/core/alpha skills/other/alpha
  assert_eq "a group move since that commit is not a change" "current 0" "$(bench_status "$c" alpha)"
  printf 'one more rule\n' >> "$c/skills/other/alpha/SKILL.md"
  assert_eq "an edit since that commit is" "changed 1" "$(bench_status "$c" alpha)"
}

# --- the real catalog -------------------------------------------------------
# The fixture cases prove the contract; this one proves the catalog that ships
# actually satisfies it.

case_real_catalog_is_sound() {
  local status
  "$ROOT/scripts/check.sh" >/dev/null 2>&1; status=$?
  assert_eq "the shipped catalog passes its own check" "0" "$status"
}

# check.sh reads frontmatter by hand; installers use a real YAML parser and reject the whole package
# when one file fails it. Parse every file the way they do, so no fault the hand reader misses ships.
case_real_catalog_frontmatter_parses_as_yaml() {
  local out
  if ! command -v ruby >/dev/null 2>&1; then
    fail "no YAML parser: install ruby so every frontmatter can be parsed as installers parse it"
    return
  fi
  out="$(cd "$ROOT" && ruby -ryaml -e '
    bad = 0
    ARGV.each do |f|
      fm = File.read(f)[/\A---\n(.*?)\n---\n/m, 1]
      begin
        data = YAML.safe_load(fm.to_s)
        raise "frontmatter is not a mapping" unless data.is_a?(Hash)
        raise "description is not text" unless data["description"].is_a?(String)
      rescue Exception => e
        puts "#{f}: #{e.message}"; bad += 1
      end
    end
    puts "#{ARGV.size} parsed, #{bad} rejected"
  ' skills/*/*/SKILL.md subagents/*.md 2>&1)"
  assert "every frontmatter parses as YAML ($out)" grep -q " 0 rejected$" <<< "$out"
  assert "the parser read every file ($out)" test "$(ls "$ROOT"/skills/*/*/SKILL.md "$ROOT"/subagents/*.md | wc -l | tr -d ' ') parsed, 0 rejected" = "$(tail -1 <<< "$out")"
}

case_real_catalog_pushes_and_resyncs() {
  local t n; t="$(new_target)"
  "$ROOT/scripts/deploy.sh" "$t" --all >/dev/null
  n="$(ls "$t/.agents/skills" | wc -l | tr -d ' ')"
  assert_eq "every shipped skill pushes" "$("$ROOT/scripts/deploy.sh" --list | wc -l | tr -d ' ')" "$n"
  assert "a shipped skill arrives byte-identical" \
    diff -r "$ROOT/skills/development/testing-code" "$t/.agents/skills/testing-code"
  "$ROOT/scripts/deploy.sh" "$t" --sync >/dev/null
  assert_eq "a resync leaves the same set" "$n" "$(ls "$t/.agents/skills" | wc -l | tr -d ' ')"
}

# --- run --------------------------------------------------------------------
echo "deploy.sh"
for c in links_claude_to_the_one_copy pushes_an_exact_copy is_idempotent \
         clears_a_skill_before_replacing_it leaves_unnamed_skills_alone \
         applies_a_variant_overlay switching_off_a_variant_restores_the_base \
         all_pushes_every_skill sync_refreshes_only_what_is_installed \
         sync_says_so_when_nothing_is_installed dry_run_writes_nothing \
         refuses_a_missing_directory refuses_a_git_checkout refuses_an_unknown_skill_and_variant \
         will_not_clobber_a_populated_agent_home list_names_every_skill; do
  run_case "$c"
done

echo "check.sh"
for c in check_passes_a_sound_catalog check_rejects_a_directory_without_skill_md \
         check_accepts_links_and_fences_written_other_ways \
         check_rejects_a_description_not_starting_use_when check_rejects_an_unlinked_reference \
         check_rejects_a_sentence_cut_short check_rejects_a_name_without_its_group_prefix \
         check_rejects_an_unlisted_group \
         check_rejects_a_name_mismatch check_rejects_a_stub_description \
         check_rejects_a_cross_skill_reference check_rejects_an_absolute_path \
         check_rejects_drifted_rule_files \
         check_rejects_a_variant_removing_a_missing_file \
         check_rejects_a_skill_outside_a_group check_rejects_a_name_in_two_groups \
         check_rejects_a_credential check_rejects_a_real_email check_accepts_reserved_email_domains \
         check_rejects_an_integration_tool check_rejects_a_manifest_missing_a_skill \
         check_rejects_a_manifest_listing_a_missing_skill check_rejects_a_bad_manifest_version \
         check_rejects_a_subagent_name_mismatch check_rejects_an_unlisted_subagent \
         check_rejects_a_subagent_naming_a_skill \
         check_rejects_an_unquoted_colon_in_frontmatter check_rejects_an_unquoted_hash_in_frontmatter \
         check_rejects_a_leading_yaml_indicator check_rejects_an_unquoted_colon_in_a_subagent \
         check_accepts_a_quoted_colon_in_frontmatter; do
  run_case "$c"
done

echo "bench-status.sh"
for c in bench_status_reports_a_skill_never_run bench_status_skips_a_recent_unchanged_result \
         bench_status_reruns_a_changed_skill bench_status_reruns_changed_cases \
         bench_status_reruns_an_old_result bench_status_ignores_a_group_move bench_status_ignores_bytecode \
         bench_status_compares_an_unhashed_result_with_its_commit; do
  run_case "$c"
done

echo "the shipped catalog"
for c in real_catalog_is_sound real_catalog_frontmatter_parses_as_yaml real_catalog_pushes_and_resyncs; do
  run_case "$c"
done

echo
echo "$discovered discovered, $executed executed, $passed passed, $failed assertion failure(s)"
[ "$failed" -eq 0 ] || exit 1
