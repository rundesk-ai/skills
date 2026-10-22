#!/usr/bin/env bash
# Push skills from this catalog into a scratch directory, such as a benchmark run's.
#
# Never a project: a checkout gets its skills from Rundesk, which this script would fight. A
# directory inside a git work tree is refused; a project gets a skill by adding it in Rundesk,
# which installs this catalog as a package.
#
#   scripts/deploy.sh <dir> <skill> [skill...]   push the named skills
#   scripts/deploy.sh <dir> --sync               refresh whatever the directory already has
#   scripts/deploy.sh <dir> --all                push every skill in the catalog
#   scripts/deploy.sh <dir> <skill>@<variant>       push a variant
#
#   --list          name the skills in the catalog and exit
#   --dry-run       say what would change, write nothing
#
# Skills land in <dir>/.agents/skills/, which Codex and Grok read; .claude/skills is a
# symlink to it for Claude, so every agent reads one copy.
#
# A skill already there is removed before it is written, never merged: a reference
# file dropped from the catalog would otherwise survive in the target forever.
# Skills not named are left alone.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CATALOG="$ROOT/skills"

list_skills() {
  for d in "$CATALOG"/*/; do
    [ -f "$d/SKILL.md" ] && basename "$d"
  done
}

if [ "${1:-}" = "--list" ]; then
  list_skills
  exit 0
fi

DRY=0
ARGS=()
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    -h|--help) awk 'NR > 1 && !/^#/ { exit } NR > 1' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *)         ARGS+=("$a") ;;
  esac
done

if [ "${#ARGS[@]}" -lt 2 ]; then
  echo "usage: scripts/deploy.sh <dir> <skill> [skill...]   (or --all, --list)" >&2
  exit 2
fi

DEST="${ARGS[0]}"
SPECS=("${ARGS[@]:1}")

if [ ! -d "$DEST" ]; then
  echo "no such directory: $DEST" >&2
  exit 2
fi
DEST="$(cd "$DEST" && pwd)"
if ! command -v git >/dev/null 2>&1; then
  echo "deploy.sh needs git, to refuse a checkout" >&2
  exit 2
fi
if git -C "$DEST" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "$DEST is in a git checkout; projects get skills from Rundesk; add the skill to the project there" >&2
  exit 2
fi

if [ "${SPECS[0]}" = "--all" ]; then
  SPECS=()
  while IFS= read -r n; do SPECS+=("$n"); done < <(list_skills)
elif [ "${SPECS[0]}" = "--sync" ]; then
  # Refresh what is already there. The usual case is a directory that took a subset
  # months ago: --all would add skills it never asked for, and naming them again by
  # hand is how a stale one gets forgotten.
  SPECS=()
  for d in "$DEST/.agents/skills"/*/; do
    [ -f "$d/SKILL.md" ] || continue
    n="$(basename "$d")"
    [ -d "$CATALOG/$n" ] || continue          # a skill of the project's own; leave it
    SPECS+=("$n")
  done
  if [ "${#SPECS[@]}" -eq 0 ]; then
    echo "== $DEST"
    echo "  nothing from this catalog is installed — name the skills you want"
    exit 0
  fi
fi

AGENTS="$DEST/.agents/skills"
HOMES=(.claude)   # Codex and Grok read .agents/skills itself

# --- Claude's skills folder --------------------------------------------------
if [ "$DRY" -eq 0 ]; then
  mkdir -p "$AGENTS"
fi

link_home() {
  # <home>/skills points at .agents/skills so one copy serves every agent.
  local home="$1" link="$DEST/$1/skills"
  if [ -L "$link" ]; then
    return 0                                   # already a link; leave it
  fi
  if [ -d "$link" ]; then
    if [ -n "$(ls -A "$link" 2>/dev/null)" ]; then
      echo "  ~ $home/skills is a real directory with skills in it — leaving it alone"
      echo "    (move what you want to keep into .agents/skills, then delete it)"
      return 0
    fi
    [ "$DRY" -eq 0 ] && rmdir "$link"
  fi
  if [ "$DRY" -eq 1 ]; then
    echo "  + $home/skills -> ../.agents/skills"
    return 0
  fi
  mkdir -p "$DEST/$home"
  ln -s ../.agents/skills "$link"
  echo "  + $home/skills -> ../.agents/skills"
}

echo "== $DEST"
for home in "${HOMES[@]}"; do link_home "$home"; done

# --- the skills -------------------------------------------------------------
written=0
for spec in "${SPECS[@]}"; do
  name="${spec%@*}"
  variant=""
  [ "$spec" != "$name" ] && variant="${spec#*@}"

  base="$CATALOG/$name"
  if [ ! -f "$base/SKILL.md" ]; then
    echo "  ! no such skill: $name" >&2
    continue
  fi
  if [ -n "$variant" ] && [ ! -d "$base/variants/$variant" ]; then
    echo "  ! no such variant: $name@$variant" >&2
    continue
  fi

  dest="$AGENTS/$name"

  if [ "$DRY" -eq 1 ]; then
    [ -e "$dest" ] && echo "  * $name — replaced" || echo "  + $name"
    continue
  fi

  # Clear first. Replacing in place would leave behind a reference file the
  # catalog has since dropped, and nothing would ever report it.
  rm -rf "$dest"
  mkdir -p "$dest"

  # the base, minus the variant overlays that are not this target's
  (cd "$base" && tar cf - --exclude variants .) | (cd "$dest" && tar xf -)

  if [ -n "$variant" ]; then
    (cd "$base/variants/$variant" && tar cf - --exclude .remove .) | (cd "$dest" && tar xf -)
    # a narrowing variant drops base files it does not carry
    if [ -f "$base/variants/$variant/.remove" ]; then
      while IFS= read -r rel; do
        [ -z "$rel" ] && continue
        case "$rel" in \#*) continue ;; esac
        rm -rf "${dest:?}/$rel"
      done < "$base/variants/$variant/.remove"
    fi
  fi

  echo "  > $name${variant:+ (@$variant)}"
  written=$((written + 1))
done

echo
if [ "$DRY" -eq 1 ]; then
  echo "dry run — nothing written"
else
  echo "$written skill(s) pushed to $AGENTS"
fi
