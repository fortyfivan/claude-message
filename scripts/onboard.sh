#!/usr/bin/env bash
# onboard.sh — Scaffold the messaging workspace for the claude-message plugin
# Usage: bash scripts/onboard.sh <plugin-root> <project-root>
#
# Creates directories, copies templates, writes seed files, and injects
# plugin context into the project's CLAUDE.md. Idempotent and non-destructive.

PLUGIN_ROOT="${1:?Usage: onboard.sh <plugin-root> <project-root>}"
PROJECT_ROOT="${2:?Usage: onboard.sh <plugin-root> <project-root>}"

# Resolve to absolute paths
PLUGIN_ROOT="$(cd "$PLUGIN_ROOT" && pwd)"
mkdir -p "$PROJECT_ROOT"
PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd)"

created=0
skipped=0
warnings=0

report() {
  echo "$1: $2"
  case "$1" in
    CREATED) created=$((created + 1)) ;;
    SKIPPED) skipped=$((skipped + 1)) ;;
    WARNING) warnings=$((warnings + 1)) ;;
  esac
}

# ─── 1. Directories ─────────────────────────────────────────────────────────

DIRS="
messaging
messaging/categories
messaging/competitors
messaging/personas
messaging/plays
messaging/products
messaging/stories
messaging/segments
messaging/solutions
templates/messaging
templates/skills
input
research
insights
insights/scans
insights/investigations
output
output/campaigns
.claude/skills
"

for dir in $DIRS; do
  target="$PROJECT_ROOT/$dir"
  if [ -d "$target" ]; then
    report "SKIPPED" "$dir/ (exists)"
  else
    mkdir -p "$target"
    report "CREATED" "$dir/"
  fi
done

# ─── 2. Templates ───────────────────────────────────────────────────────────

# Messaging templates
if [ -d "$PLUGIN_ROOT/templates/messaging" ]; then
  for src in "$PLUGIN_ROOT"/templates/messaging/*.md; do
    [ -f "$src" ] || continue
    name="$(basename "$src")"
    dest="$PROJECT_ROOT/templates/messaging/$name"
    if [ -f "$dest" ]; then
      report "SKIPPED" "templates/messaging/$name (exists)"
    else
      cp "$src" "$dest"
      report "CREATED" "templates/messaging/$name"
    fi
  done
fi

# Skill templates — preserve category/type hierarchy
if [ -d "$PLUGIN_ROOT/templates/skills" ]; then
  SKILL_LIST="$(mktemp)"
  (cd "$PLUGIN_ROOT/templates/skills" && find . -type f -name '*.md') > "$SKILL_LIST"
  while read -r relpath; do
    relpath="${relpath#./}"
    src="$PLUGIN_ROOT/templates/skills/$relpath"
    dest="$PROJECT_ROOT/templates/skills/$relpath"
    destdir="$(dirname "$dest")"
    if [ -f "$dest" ]; then
      report "SKIPPED" "templates/skills/$relpath (exists)"
    else
      mkdir -p "$destdir"
      cp "$src" "$dest"
      report "CREATED" "templates/skills/$relpath"
    fi
  done < "$SKILL_LIST"
  rm -f "$SKILL_LIST"
fi

# ─── 3. Seed files ──────────────────────────────────────────────────────────

for seed in config.md tracker.md; do
  src="$PLUGIN_ROOT/templates/insights/$seed"
  dest="$PROJECT_ROOT/insights/$seed"
  if [ -f "$dest" ]; then
    report "SKIPPED" "insights/$seed (exists)"
  elif [ -f "$src" ]; then
    cp "$src" "$dest"
    report "CREATED" "insights/$seed"
  fi
done

# ─── 4. CLAUDE.md injection ─────────────────────────────────────────────────

CLAUDE_MD="$PROJECT_ROOT/CLAUDE.md"
CONTEXT_SRC="$PLUGIN_ROOT/templates/onboard/claude-message-context.md"
MARKER_START="<!-- claude-message:start -->"
MARKER_END="<!-- claude-message:end -->"

if [ -f "$CONTEXT_SRC" ]; then
  CONTEXT_BLOCK="$(cat "$CONTEXT_SRC")"

  if [ ! -f "$CLAUDE_MD" ]; then
    # No CLAUDE.md — create with markers wrapping the context block
    printf '%s\n%s\n%s\n' "$MARKER_START" "$CONTEXT_BLOCK" "$MARKER_END" > "$CLAUDE_MD"
    report "CREATED" "CLAUDE.md (with plugin context)"

  elif ! grep -qF "$MARKER_START" "$CLAUDE_MD"; then
    # CLAUDE.md exists, no markers — append
    printf '\n%s\n%s\n%s\n' "$MARKER_START" "$CONTEXT_BLOCK" "$MARKER_END" >> "$CLAUDE_MD"
    report "UPDATED" "CLAUDE.md (appended plugin context)"

  else
    # CLAUDE.md exists, markers present — replace between markers (inclusive)
    # Preserve populated writing profile if bootstrap has written one
    PROFILE_START="<!-- claude-message:profile:start -->"
    PROFILE_END="<!-- claude-message:profile:end -->"
    PROFILE_PLACEHOLDER="Run \`/claude-message:bootstrap\` to generate your writing profile from the messaging house."

    TMPPROFILE="$(mktemp)"
    if grep -qF "$PROFILE_START" "$CLAUDE_MD"; then
      awk -v ps="$PROFILE_START" -v pe="$PROFILE_END" \
        'BEGIN { capture=0 }
         index($0, ps) == 1 { capture=1; next }
         index($0, pe) == 1 { capture=0; next }
         capture { print }' "$CLAUDE_MD" > "$TMPPROFILE"
    fi

    TMPINJECT="$(mktemp)"
    printf '%s\n%s\n%s\n' "$MARKER_START" "$CONTEXT_BLOCK" "$MARKER_END" > "$TMPINJECT"

    # If the existing profile is populated (not the placeholder), swap it into the new injection
    if [ -s "$TMPPROFILE" ] && ! grep -qxF "$PROFILE_PLACEHOLDER" "$TMPPROFILE"; then
      TMPRESULT="$(mktemp)"
      awk -v ps="$PROFILE_START" -v pe="$PROFILE_END" -v pfile="$TMPPROFILE" \
        'index($0, ps) == 1 {
           print
           while ((getline pline < pfile) > 0) print pline
           close(pfile)
           # skip template placeholder lines until profile end marker
           skip=1
           next
         }
         index($0, pe) == 1 { skip=0; print; next }
         skip { next }
         { print }' "$TMPINJECT" > "$TMPRESULT"
      mv "$TMPRESULT" "$TMPINJECT"
    fi

    rm -f "$TMPPROFILE"

    awk -v tmpfile="$TMPINJECT" \
        -v ms="$MARKER_START" \
        -v me="$MARKER_END" \
        'BEGIN { skip=0; replaced=0 }
         index($0, ms) == 1 {
           skip=1
           if (!replaced) {
             while ((getline line < tmpfile) > 0) print line
             close(tmpfile)
             replaced=1
           }
           next
         }
         index($0, me) == 1 { skip=0; next }
         !skip { print }' "$CLAUDE_MD" > "$CLAUDE_MD.tmp"

    rm -f "$TMPINJECT"
    mv "$CLAUDE_MD.tmp" "$CLAUDE_MD"
    report "UPDATED" "CLAUDE.md (replaced plugin context)"
  fi
fi

# ─── 5. Warnings ────────────────────────────────────────────────────────────

# Unexpected directories inside messaging/
EXPECTED_SUBDIRS="categories competitors personas plays products stories segments solutions"

if [ -d "$PROJECT_ROOT/messaging" ]; then
  for entry in "$PROJECT_ROOT"/messaging/*/; do
    [ -d "$entry" ] || continue
    dirname="$(basename "$entry")"
    found=0
    for expected in $EXPECTED_SUBDIRS; do
      if [ "$dirname" = "$expected" ]; then
        found=1
        break
      fi
    done
    if [ "$found" -eq 0 ]; then
      report "WARNING" "unexpected directory messaging/$dirname/"
    fi
  done
fi

# Existing .claude/skills/ categories that match plugin skill categories
if [ -d "$PROJECT_ROOT/.claude/skills" ] && [ -d "$PLUGIN_ROOT/templates/skills" ]; then
  for plugin_cat in "$PLUGIN_ROOT"/templates/skills/*/; do
    [ -d "$plugin_cat" ] || continue
    catname="$(basename "$plugin_cat")"
    if [ -d "$PROJECT_ROOT/.claude/skills/$catname" ]; then
      report "WARNING" "existing .claude/skills/$catname/ may conflict with plugin skills"
    fi
  done
fi

# Non-empty messaging/*.md files that already exist
if [ -d "$PROJECT_ROOT/messaging" ]; then
  for mdfile in "$PROJECT_ROOT"/messaging/*.md; do
    [ -f "$mdfile" ] || continue
    name="$(basename "$mdfile")"
    if [ -s "$mdfile" ]; then
      report "WARNING" "messaging/$name already exists and is non-empty (potential schema conflict)"
    fi
  done
fi

# ─── Summary ────────────────────────────────────────────────────────────────

echo "DONE: $created created, $skipped skipped, $warnings warnings"
exit 0
