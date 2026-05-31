#!/usr/bin/env python3
"""
validate.py — claude-message v1 structural validation.

Runs the 24 checks defined in the v2-refactor PRD against the repository.
stdlib only — no external dependencies. Same script that runs in CI also
runs locally for fast feedback before push.

Exit codes:
    0 — all enforced checks pass (warnings allowed)
    1 — one or more enforced checks failed

Usage:
    python scripts/validate.py                # full validation
    python scripts/validate.py --quiet        # only output errors and summary
    python scripts/validate.py --no-warn      # exit non-zero on warnings too
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
AGENTS_DIR = REPO_ROOT / ".claude" / "agents"
COMMANDS_DIR = REPO_ROOT / ".claude" / "commands"
MESSAGING_DIR = REPO_ROOT / "messaging"
PILLARS_DIR = MESSAGING_DIR / "pillars"
ASSETS_DIR = MESSAGING_DIR / "assets"
TEMPLATES_DIR = REPO_ROOT / "templates"
TEMPLATE_ASSETS_DIR = TEMPLATES_DIR / "assets"
TEMPLATE_PILLARS_DIR = TEMPLATES_DIR / "pillars"
TEMPLATE_COLLECTIONS_DIR = TEMPLATES_DIR / "collections"
MESSAGE_MD = REPO_ROOT / "MESSAGE.md"
VARIANT_LIKELY_ASSETS = {
    "blog-post",
    "customer-story",
    "whitepaper",
    "landing-page",
    "email",
    "one-pager",
    "social-post",
}
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"
BRAND_DIR = REPO_ROOT / "brand"
BRAND_DESIGN_MD = BRAND_DIR / "DESIGN.md"
TEMPLATE_DESIGN_MD = TEMPLATES_DIR / "DESIGN-template.md"

# Standard production targets shipped with claude-message.
STANDARD_PRODUCTION_TARGETS = {"web", "email", "print"}

ALLOWED_SKILL_CATEGORIES = {"system", "builders", "messaging", "tasks", "craft"}
PILLAR_NAMES_REQUIRING_COLLECTION_TABLES = {"position", "people", "portfolio", "proof"}
ALL_PILLAR_NAMES = {"profile", "pitch", "position", "people", "portfolio", "proof"}
KEBAB_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
DUPLICATE_WINDOW = 5  # lines per shared sequence

# Documentation-only paths where stale-rename refs are tolerated.
DOC_PATHS_PERMISSIVE = {REPO_ROOT / "CHANGELOG.md"}

# Canonical text every messaging-system-conformant skill carries.
# Source of truth: templates/messaging-system-reference.md
BLURB_CANONICAL_PHRASE = "This skill operates against a MESSAGE.md-conformant messaging system."
BLURB_HEADING = "## Messaging System Reference"

# Skill-length thresholds (warn over). Builders allow more headroom for orchestration logic.
SKILL_LENGTH_THRESHOLDS = {
    "builders": 400,
    "messaging": 400,
    "system": 500,  # run-investigation legitimately runs long; tune over time
    "tasks": 250,
    "craft": 300,
}

# Path strings to scan for restatement in skill body text.
RESTATEMENT_PATH_PATTERNS = [
    re.compile(r"`?messaging/pillars/`?"),
    re.compile(r"`?messaging/collections/`?"),
    re.compile(r"`?messaging/assets/`?"),
]


def discover_markdown(root: Path) -> list[Path]:
    """Return all .md files under root, skipping hidden/_archive and dev refs."""
    files: list[Path] = []
    for path in root.rglob("*.md"):
        rel = path.relative_to(REPO_ROOT)
        # Skip the dev/ reference directory and any archive/hidden dirs.
        parts = rel.parts
        if parts and (parts[0] == "dev" or parts[0].startswith(".") or "_archive" in parts):
            continue
        files.append(path)
    return files


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return ""


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Minimal YAML frontmatter parser. Returns dict of scalar fields or None."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    block = text[4:end]
    out: dict[str, str] = {}
    for line in block.splitlines():
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        out[key.strip()] = value.strip().strip('"').strip("'")
    return out


class Report:
    """Collects findings and prints a structured summary."""

    def __init__(self) -> None:
        self.errors: list[tuple[str, str]] = []   # (check_id, message)
        self.warnings: list[tuple[str, str]] = []
        self.checks_run: list[str] = []

    def begin(self, check_id: str) -> None:
        self.checks_run.append(check_id)

    def err(self, check_id: str, message: str) -> None:
        self.errors.append((check_id, message))

    def warn(self, check_id: str, message: str) -> None:
        self.warnings.append((check_id, message))

    def emit(self, *, quiet: bool, treat_warnings_as_errors: bool) -> int:
        if not quiet:
            print(f"Ran {len(self.checks_run)} checks: {', '.join(self.checks_run)}")
            print()
        if self.errors:
            print(f"❌ {len(self.errors)} error(s):")
            for check, msg in self.errors:
                print(f"  [{check}] {msg}")
        if self.warnings:
            print(f"⚠ {len(self.warnings)} warning(s):")
            for check, msg in self.warnings:
                print(f"  [{check}] {msg}")
        if not self.errors and not self.warnings:
            print("✓ All checks passed.")
        exit_code = 1 if self.errors else 0
        if treat_warnings_as_errors and self.warnings:
            exit_code = 1
        return exit_code


# ----- Checks -----

def check_taxonomy(report: Report) -> None:
    """#1 Every skill is under system/, builders/, messaging/, tasks/, or craft/."""
    report.begin("taxonomy")
    if not SKILLS_DIR.exists():
        return
    for child in SKILLS_DIR.iterdir():
        if child.is_dir() and child.name not in ALLOWED_SKILL_CATEGORIES:
            report.err("taxonomy", f"Unexpected skill category: .claude/skills/{child.name}/")


def check_no_build(report: Report) -> None:
    """#3 No skill or doc references the removed /build command."""
    report.begin("no-build")
    pattern = re.compile(r"/build\s+(campaign|launch|play)|\.claude/commands/build\.md")
    _scan_pattern(
        report, "no-build", pattern,
        message_fmt="references removed /build command in {path}:{line}",
        roots=[SKILLS_DIR, AGENTS_DIR, COMMANDS_DIR, MESSAGE_MD, CLAUDE_MD],
        permissive=DOC_PATHS_PERMISSIVE,
    )


def check_no_old_pillar_names(report: Report) -> None:
    """#4 No skill or doc treats `space`, `motion`, or `audience` as pillar names."""
    report.begin("no-old-pillars")
    pattern = re.compile(r"pillars/(space|motion|audience)\.md|\b(space|motion|audience) pillar\b", re.IGNORECASE)
    _scan_pattern(
        report, "no-old-pillars", pattern,
        message_fmt="references old pillar name in {path}:{line}",
        roots=[SKILLS_DIR, AGENTS_DIR, COMMANDS_DIR, MESSAGE_MD, CLAUDE_MD],
        permissive=DOC_PATHS_PERMISSIVE,
    )


def check_frontmatter(report: Report) -> None:
    """#5 Every SKILL.md has required frontmatter fields with valid bounds."""
    report.begin("frontmatter")
    if not SKILLS_DIR.exists():
        return
    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        rel = skill_md.relative_to(REPO_ROOT)
        text = read_text(skill_md)
        fm = parse_frontmatter(text)
        if fm is None:
            report.err("frontmatter", f"{rel}: missing YAML frontmatter")
            continue
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if not name:
            report.err("frontmatter", f"{rel}: frontmatter missing 'name'")
        elif len(name) >= 64:
            report.err("frontmatter", f"{rel}: 'name' must be under 64 chars (got {len(name)})")
        elif not KEBAB_RE.match(name):
            report.err("frontmatter", f"{rel}: 'name' must be kebab-case (got '{name}')")
        if not desc:
            report.err("frontmatter", f"{rel}: frontmatter missing 'description'")
        elif len(desc) > 1024:
            report.err("frontmatter", f"{rel}: 'description' must be under 1024 chars (got {len(desc)})")


def check_anatomy(report: Report) -> None:
    """#6 Every skill is a folder containing SKILL.md. No bare .md files."""
    report.begin("anatomy")
    if not SKILLS_DIR.exists():
        return
    for category in SKILLS_DIR.iterdir():
        if not category.is_dir():
            continue
        for skill in category.rglob("*"):
            if not skill.is_file() or skill.suffix != ".md":
                continue
            # Type files under types/ and README.md files are not skills.
            parts = skill.relative_to(SKILLS_DIR).parts
            if "types" in parts or skill.name == "README.md":
                continue
            if skill.name != "SKILL.md":
                report.err("anatomy", f".claude/skills/{skill.relative_to(SKILLS_DIR)}: only SKILL.md, README.md, and types/*.md are valid skill files")


def check_cross_references(report: Report) -> None:
    """#7 references/, scripts/, templates/ paths in SKILL.md exist (skill-relative OR repo-root)."""
    report.begin("cross-references")
    pattern = re.compile(r"`(references|scripts|templates)/[^`\s]+`")
    if not SKILLS_DIR.exists():
        return
    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        rel = skill_md.relative_to(REPO_ROOT)
        text = read_text(skill_md)
        for match in pattern.finditer(text):
            ref = match.group(0).strip("`")
            # Skip references with bracket placeholders — those are template/example paths, not literal.
            if "[" in ref or "]" in ref:
                continue
            # Resolve as repo-root-relative first (for top-level templates/), then fall back to skill-relative.
            target_root = REPO_ROOT / ref
            target_local = skill_md.parent / ref
            if not target_root.exists() and not target_local.exists():
                report.warn("cross-references", f"{rel}: references missing path '{ref}'")


def check_asset_variants_warn(report: Report) -> None:
    """#8 Warn when variant-likely assets (blog-post, paper, story, web pages) lack a variants/ directory."""
    report.begin("asset-variants-warn")
    if not ASSETS_DIR.exists():
        return
    for asset_dir in ASSETS_DIR.iterdir():
        if not asset_dir.is_dir():
            continue
        slug = asset_dir.name
        if slug not in VARIANT_LIKELY_ASSETS:
            continue
        variants_dir = asset_dir / "variants"
        if not variants_dir.exists() or not any(variants_dir.glob("*.md")):
            report.warn(
                "asset-variants-warn",
                f"messaging/assets/{slug}/ has no variants/ — variant-likely assets typically benefit from at least one variant. "
                f"Add via `/design asset {slug} --add-variant [name]`.",
            )


def check_assets(report: Report) -> None:
    """#9 Every content type in MESSAGE.md's Assets table maps to either a populated asset folder OR a template."""
    report.begin("assets")
    if not MESSAGE_MD.exists():
        report.err("assets", "MESSAGE.md not found")
        return
    text = read_text(MESSAGE_MD)
    section_match = re.search(r"^##\s+Assets\s*$([\s\S]+?)(^##\s|\Z)", text, re.MULTILINE)
    if section_match is None:
        report.err("assets", "MESSAGE.md has no '## Assets' section")
        return
    body = section_match.group(1)
    # Find table rows: | content type | `default` | alternatives |
    row_re = re.compile(r"^\|\s*([a-z][a-z0-9-]*)\s*\|\s*`?([a-z][a-z0-9-]*)`?\s*\|.*\|$", re.MULTILINE)
    rows = row_re.findall(body)
    seen = set()
    for content_type, default_slug in rows:
        if default_slug in seen:
            continue
        seen.add(default_slug)
        asset_md = ASSETS_DIR / default_slug / "asset.md"
        template_md = TEMPLATE_ASSETS_DIR / f"{default_slug}-template" / "asset.md"
        if not asset_md.exists() and not template_md.exists():
            report.warn(
                "assets",
                f"Assets default '{default_slug}' (content type: {content_type}) has neither messaging/assets/{default_slug}/asset.md nor templates/assets/{default_slug}-template/asset.md",
            )


def check_no_format_paths(report: Report) -> None:
    """#13 No references to retired `messaging/formats/`, `format.md` (as asset spec), or `## Format Routing` heading."""
    report.begin("no-format-paths")
    pattern = re.compile(r"messaging/formats/|templates/formats/|/format\.md\b|## Format Routing")
    _scan_pattern(
        report, "no-format-paths", pattern,
        message_fmt="references retired format paths/heading in {path}:{line}",
        roots=[SKILLS_DIR, AGENTS_DIR, COMMANDS_DIR, MESSAGE_MD, CLAUDE_MD],
        permissive=DOC_PATHS_PERMISSIVE,
    )


def check_no_legacy_commands(report: Report) -> None:
    """#14 No references to retired commands `/campaign`, `/launch`, `/play`, `/compose`, `/health`, `/investigate`, `/update` (allowed in CHANGELOG)."""
    report.begin("no-legacy-commands")
    pattern = re.compile(r"/(campaign|launch|play|compose|health|investigate|update)(?:\s|`|$)")
    _scan_pattern(
        report, "no-legacy-commands", pattern,
        message_fmt="references retired command in {path}:{line}",
        roots=[SKILLS_DIR, AGENTS_DIR, COMMANDS_DIR, MESSAGE_MD, CLAUDE_MD],
        permissive=DOC_PATHS_PERMISSIVE,
    )


def check_asset_default_variants(report: Report) -> None:
    """#15 Asset frontmatter `default-variant` (when non-empty) must match an existing file in the asset's variants/ directory."""
    report.begin("asset-default-variants")
    if not ASSETS_DIR.exists():
        return
    for asset_dir in ASSETS_DIR.iterdir():
        if not asset_dir.is_dir():
            continue
        asset_md = asset_dir / "asset.md"
        if not asset_md.exists():
            continue
        text = read_text(asset_md)
        fm = parse_frontmatter(text)
        if fm is None:
            continue
        default_variant = fm.get("default-variant", "").strip()
        if not default_variant:
            continue
        variant_file = asset_dir / "variants" / f"{default_variant}.md"
        if not variant_file.exists():
            report.err(
                "asset-default-variants",
                f"messaging/assets/{asset_dir.name}/asset.md declares default-variant '{default_variant}' "
                f"but variants/{default_variant}.md does not exist",
            )


def check_asset_variants_table(report: Report) -> None:
    """#21 For populated assets with variants/, asset.md must have a `## Variants` table; table rows must reference real variant files; exactly one row marked default; default-variant frontmatter must agree."""
    report.begin("asset-variants-table")
    if not ASSETS_DIR.exists():
        return
    for asset_dir in ASSETS_DIR.iterdir():
        if not asset_dir.is_dir():
            continue
        asset_md = asset_dir / "asset.md"
        if not asset_md.exists():
            continue
        variants_dir = asset_dir / "variants"
        has_variants_dir = variants_dir.exists() and any(variants_dir.glob("*.md"))
        text = read_text(asset_md)
        m = re.search(r"^##\s+Variants\b.*?$\n(.*?)(?=^##\s+\S|\Z)", text, re.MULTILINE | re.DOTALL)
        has_section = m is not None
        if has_variants_dir and not has_section:
            report.warn(
                "asset-variants-table",
                f"messaging/assets/{asset_dir.name}/asset.md has variants/ but no `## Variants` section",
            )
            continue
        if not has_section:
            continue
        body = m.group(1)
        # Parse rows: | Variant | File | Default | Description |
        row_re = re.compile(r"^\|\s*([a-z][a-z0-9-]*)\s*\|\s*(variants/[a-z0-9-]+\.md)\s*\|\s*(✓|)\s*\|.*\|$", re.MULTILINE)
        rows = row_re.findall(body)
        if not rows:
            # Either the table is the placeholder or malformed — only warn when there are actual variants
            if has_variants_dir:
                report.warn(
                    "asset-variants-table",
                    f"messaging/assets/{asset_dir.name}/asset.md `## Variants` table is empty but variants/ contains files",
                )
            continue
        # Verify file column references exist
        default_count = 0
        default_slug_in_table: str | None = None
        for variant_slug, file_ref, default_marker in rows:
            target = asset_dir / file_ref
            if not target.exists():
                report.err(
                    "asset-variants-table",
                    f"messaging/assets/{asset_dir.name}/asset.md Variants row '{variant_slug}' references missing file '{file_ref}'",
                )
            if default_marker == "✓":
                default_count += 1
                default_slug_in_table = variant_slug
        if default_count > 1:
            report.err(
                "asset-variants-table",
                f"messaging/assets/{asset_dir.name}/asset.md `## Variants` table has {default_count} rows marked default (must be exactly one)",
            )
        # Verify default matches frontmatter
        fm = parse_frontmatter(text)
        if fm is not None and default_slug_in_table is not None:
            fm_default = fm.get("default-variant", "").strip()
            if fm_default and fm_default != default_slug_in_table:
                report.err(
                    "asset-variants-table",
                    f"messaging/assets/{asset_dir.name}/asset.md: `## Variants` table default '{default_slug_in_table}' "
                    f"does not match frontmatter `default-variant: {fm_default}`",
                )


def _parse_yaml_list(text: str, key: str) -> list[str]:
    """Minimal parser for a YAML list field in frontmatter. Handles `key: [a, b]` and multi-line `key:\\n  - a\\n  - b`."""
    if not text.startswith("---\n"):
        return []
    end = text.find("\n---", 4)
    if end == -1:
        return []
    block = text[4:end]
    # Inline form: key: [a, b, c]
    inline = re.search(rf"^{re.escape(key)}:\s*\[(.*?)\]\s*$", block, re.MULTILINE)
    if inline:
        items = [i.strip().strip('"').strip("'") for i in inline.group(1).split(",")]
        return [i for i in items if i]
    # Multi-line form
    multiline = re.search(rf"^{re.escape(key)}:\s*$\n((?:\s*-\s*\S.*\n?)+)", block, re.MULTILINE)
    if multiline:
        items = []
        for line in multiline.group(1).splitlines():
            m = re.match(r"\s*-\s*(.*)", line)
            if m:
                items.append(m.group(1).strip().strip('"').strip("'"))
        return items
    return []


def check_pillar_sections(report: Report) -> None:
    """#10 Every pillar contains required sections. WARN-ONLY per project policy."""
    report.begin("pillar-sections")
    if not PILLARS_DIR.exists():
        return
    required_universal = {"## Messaging Blocks", "## Writing Guidelines", "## Messaging Rules"}
    for pillar_md in sorted(PILLARS_DIR.glob("*.md")):
        rel = pillar_md.relative_to(REPO_ROOT)
        text = read_text(pillar_md)
        pillar_name = pillar_md.stem
        headings = set(re.findall(r"^##\s+\S.*$", text, re.MULTILINE))
        for required in required_universal:
            if not any(h.startswith(required) for h in headings):
                report.warn("pillar-sections", f"{rel}: missing required section '{required}'")
        if pillar_name in PILLAR_NAMES_REQUIRING_COLLECTION_TABLES:
            if not any(h.startswith("## Collection Tables") for h in headings):
                report.warn("pillar-sections", f"{rel}: missing required '## Collection Tables' section (Position/People/Portfolio/Proof)")


def check_templates(report: Report) -> None:
    """#12 The templates/ directory has the expected shape and templates declare required sections."""
    report.begin("templates")
    if not TEMPLATES_DIR.exists():
        report.err("templates", "templates/ directory does not exist")
        return
    # Pillar templates
    if TEMPLATE_PILLARS_DIR.exists():
        for pillar in ALL_PILLAR_NAMES:
            t = TEMPLATE_PILLARS_DIR / f"{pillar}-template.md"
            if not t.exists():
                report.warn("templates", f"missing pillar template: {t.relative_to(REPO_ROOT)}")
            else:
                text = read_text(t)
                for required in ("## Messaging Blocks", "## Writing Guidelines", "## Messaging Rules"):
                    if required not in text:
                        report.warn("templates", f"{t.relative_to(REPO_ROOT)}: missing section '{required}'")
    else:
        report.err("templates", "templates/pillars/ does not exist")
    # Collection templates
    if TEMPLATE_COLLECTIONS_DIR.exists():
        for ctype in ("category", "competitor", "persona", "product", "report", "segment", "solution", "story"):
            t = TEMPLATE_COLLECTIONS_DIR / f"{ctype}-template.md"
            if not t.exists():
                report.warn("templates", f"missing collection template: {t.relative_to(REPO_ROOT)}")
    else:
        report.err("templates", "templates/collections/ does not exist")
    # Asset templates — each is a folder with asset.md + README.md
    # Sections required depend on whether the asset is variant-likely (Structure + CTA live in variants)
    # or atomic (Structure + CTA live in asset.md by necessity).
    if TEMPLATE_ASSETS_DIR.exists():
        for entry in TEMPLATE_ASSETS_DIR.iterdir():
            if not entry.is_dir() or not entry.name.endswith("-template"):
                continue
            slug = entry.name[: -len("-template")]
            fmt = entry / "asset.md"
            readme = entry / "README.md"
            if not fmt.exists():
                report.err("templates", f"{entry.relative_to(REPO_ROOT)}/ missing asset.md")
            if not readme.exists():
                report.warn("templates", f"{entry.relative_to(REPO_ROOT)}/ missing README.md (author guidance)")
            if not fmt.exists():
                continue
            text = read_text(fmt)
            is_variant_likely = slug in VARIANT_LIKELY_ASSETS
            if is_variant_likely:
                # Variant-likely envelope: Conventions + Frontmatter requirements + Variants table
                for required in ("## Conventions", "## Frontmatter requirements", "## Variants"):
                    if required not in text:
                        report.warn("templates", f"{fmt.relative_to(REPO_ROOT)}: missing section '{required}'")
                # Forbid Structure / CTA on variant-likely envelope (they belong in variants)
                for forbidden in ("## Structure", "## CTA conventions"):
                    if forbidden in text:
                        report.warn(
                            "templates",
                            f"{fmt.relative_to(REPO_ROOT)}: variant-likely asset templates should not declare '{forbidden}' — that section belongs in variants/",
                        )
            else:
                # Atomic envelope: Structure + Conventions + Frontmatter requirements + CTA conventions
                for required in ("## Structure", "## Conventions", "## Frontmatter requirements", "## CTA conventions"):
                    if required not in text:
                        report.warn("templates", f"{fmt.relative_to(REPO_ROOT)}: missing section '{required}'")
    else:
        report.err("templates", "templates/assets/ does not exist")
    # Variant templates — variant-likely asset templates include a variants/variant-template.md
    if TEMPLATE_ASSETS_DIR.exists():
        for slug in VARIANT_LIKELY_ASSETS:
            variant_template = TEMPLATE_ASSETS_DIR / f"{slug}-template" / "variants" / "variant-template.md"
            if not variant_template.exists():
                report.warn("templates", f"missing variant template: {variant_template.relative_to(REPO_ROOT)}")
            else:
                text = read_text(variant_template)
                for required in ("## When to use", "## Voice notes", "## Structure", "## CTA conventions"):
                    if required not in text:
                        report.warn("templates", f"{variant_template.relative_to(REPO_ROOT)}: missing section '{required}'")


def check_message_sections(report: Report) -> None:
    """#16 MESSAGE.md contains all 9 required sections (Loading lives in CLAUDE.md)."""
    report.begin("message-sections")
    if not MESSAGE_MD.exists():
        report.err("message-sections", "MESSAGE.md does not exist at repo root")
        return
    text = read_text(MESSAGE_MD)
    required_sections = [
        "## Attributes",
        "## Facts",
        "## ICP",
        "## Glossary",
        "## Brand Guardrails",
        "## Scenarios",
        "## Pillars",
        "## Collections",
        "## Assets",
    ]
    if "## Loading" in text:
        report.warn(
            "message-sections",
            "MESSAGE.md still contains a '## Loading' section — relocated to CLAUDE.md Progressive Loading per v1.4.0. Remove from MESSAGE.md.",
        )
    headings = set(re.findall(r"^##\s+\S.*$", text, re.MULTILINE))
    for section in required_sections:
        if not any(h.startswith(section) for h in headings):
            report.err("message-sections", f"MESSAGE.md: missing required section '{section}'")
    # Frontmatter required
    fm = parse_frontmatter(text)
    if fm is None:
        report.err("message-sections", "MESSAGE.md: missing or malformed frontmatter")
    else:
        for field in ("company", "version", "maintained-by", "last-reviewed"):
            if field not in fm:
                report.warn("message-sections", f"MESSAGE.md frontmatter: missing field '{field}'")


def check_scenarios_dimensions(report: Report) -> None:
    """#17 MESSAGE.md Scenarios section declares exactly 5 dimensions with spec-fixed enum values present."""
    report.begin("scenarios-dimensions")
    if not MESSAGE_MD.exists():
        return
    text = read_text(MESSAGE_MD)
    # Extract the Scenarios section body up to the next H2.
    m = re.search(r"^##\s+Scenarios\b.*?$\n(.*?)(?=^##\s+\S|\Z)", text, re.MULTILINE | re.DOTALL)
    if not m:
        report.err("scenarios-dimensions", "MESSAGE.md: no Scenarios section found")
        return
    body = m.group(1)
    required_dimensions = [
        "Compelling event",
        "Topic maturity",
        "Market moment",
        "Strategic shape",
        "Content lens",
    ]
    for dim in required_dimensions:
        if not re.search(rf"^\|\s*{re.escape(dim)}\s*\|", body, re.MULTILINE):
            report.err("scenarios-dimensions", f"MESSAGE.md Scenarios: missing dimension row '{dim}'")
    # Spec-fixed enum values that must appear for the three spec-defined dimensions.
    spec_fixed_values = {
        "Topic maturity": ["nascent", "emerging", "established", "mature"],
        "Strategic shape": [
            "competitive-takeout", "new-product-introduction", "brand-campaign",
            "category-creation", "customer-expansion", "crisis-response",
            "thought-leadership", "demand-generation",
        ],
        "Content lens": ["Awareness", "Acquisition", "Activation", "Adoption", "Advocacy", "Amplification"],
    }
    for dim, values in spec_fixed_values.items():
        row_match = re.search(rf"^\|\s*{re.escape(dim)}\s*\|(.+?)\|\s*$", body, re.MULTILINE)
        if not row_match:
            continue
        row_text = row_match.group(1)
        for value in values:
            if value not in row_text:
                report.warn("scenarios-dimensions", f"MESSAGE.md Scenarios: dimension '{dim}' missing spec value '{value}'")


def check_glossary_discipline(report: Report) -> None:
    """#18 Warn when product/competitor/customer/persona/category names appear in MESSAGE.md Glossary."""
    report.begin("glossary-discipline")
    if not MESSAGE_MD.exists():
        return
    text = read_text(MESSAGE_MD)
    m = re.search(r"^##\s+Glossary\b.*?$\n(.*?)(?=^##\s+\S|\Z)", text, re.MULTILINE | re.DOTALL)
    if not m:
        return
    body = m.group(1)
    # Extract bolded terms — the pattern `- **Term**` indicates a glossary entry.
    glossary_terms = set()
    for line in body.splitlines():
        bm = re.match(r"\s*-\s*\*\*([^*]+)\*\*", line)
        if bm:
            term = bm.group(1).strip().lower()
            # Skip the template placeholder.
            if term.startswith("[instructions"):
                continue
            glossary_terms.add(term)
    if not glossary_terms:
        return
    # Cross-check against known collection items if any exist.
    collections_dir = MESSAGING_DIR / "collections"
    if not collections_dir.exists():
        return
    for ctype_subdir in ("products", "competitors", "stories", "personas", "categories"):
        cdir = collections_dir / ctype_subdir
        if not cdir.exists():
            continue
        for cfile in cdir.glob("*.md"):
            if cfile.name == ".gitkeep":
                continue
            slug = cfile.stem.replace("-", " ").lower()
            if slug in glossary_terms:
                report.warn(
                    "glossary-discipline",
                    f"MESSAGE.md Glossary: term '{slug}' appears to be a {ctype_subdir[:-1]} name "
                    f"(see {cfile.relative_to(REPO_ROOT)}) — collection-scoped terms belong in their collection",
                )


def check_claude_md_sections(report: Report) -> None:
    """#19 CLAUDE.md contains the operating-guide sections that own loading + path conventions."""
    report.begin("claude-md-sections")
    if not CLAUDE_MD.exists():
        report.err("claude-md-sections", "CLAUDE.md does not exist at repo root")
        return
    text = read_text(CLAUDE_MD)
    required_sections = [
        "## Always-On Foundation",
        "## Progressive Loading",
        "## File Path Conventions",
        "## Skill Recognition",
    ]
    headings = set(re.findall(r"^##\s+\S.*$", text, re.MULTILINE))
    for section in required_sections:
        if not any(h.startswith(section) for h in headings):
            report.err("claude-md-sections", f"CLAUDE.md: missing required section '{section}'")
    body = text
    # Progressive Loading should describe the two-step protocol (presence check, not exact text).
    if "Infer the scenario" not in body:
        report.warn("claude-md-sections", "CLAUDE.md Progressive Loading: missing 'Infer the scenario' step")
    if "Assemble the" not in body:
        report.warn("claude-md-sections", "CLAUDE.md Progressive Loading: missing 'Assemble the ...' step")


SPEC_FIXED_SCENARIO_VALUES = {
    "topic-maturity": {"nascent", "emerging", "established", "mature"},
    "strategic-shape": {
        "competitive-takeout", "new-product-introduction", "brand-campaign",
        "category-creation", "customer-expansion", "crisis-response",
        "thought-leadership", "demand-generation",
    },
    "content-lens": {"Awareness", "Acquisition", "Activation", "Adoption", "Advocacy", "Amplification"},
}


def check_brief_scenarios(report: Report) -> None:
    """#20 If briefs exist in output/{campaigns,launches,plays}/*/brief.md, each must declare a scenario block."""
    report.begin("brief-scenarios")
    output_root = REPO_ROOT / "output"
    if not output_root.exists():
        return
    brief_glob_roots = [output_root / sub for sub in ("campaigns", "launches", "plays")]
    required_keys = {"compelling-event", "topic-maturity", "market-moment", "strategic-shape", "content-lens"}
    for root in brief_glob_roots:
        if not root.exists():
            continue
        for brief in root.glob("*/brief.md"):
            text = read_text(brief)
            rel = brief.relative_to(REPO_ROOT)
            if "scenario:" not in text:
                report.warn("brief-scenarios", f"{rel}: missing 'scenario:' frontmatter block")
                continue
            # Look for the scenario block — minimal multi-line parser
            m = re.search(r"^scenario:\s*\n((?:\s+\S.*\n?)+)", text, re.MULTILINE)
            if not m:
                report.warn("brief-scenarios", f"{rel}: scenario field present but block malformed")
                continue
            block = m.group(1)
            present_keys = set(re.findall(r"^\s+([a-z-]+):", block, re.MULTILINE))
            missing = required_keys - present_keys
            if missing:
                report.warn("brief-scenarios", f"{rel}: scenario missing keys: {sorted(missing)}")
            # Validate spec-fixed enums (when value is non-null)
            for key, allowed in SPEC_FIXED_SCENARIO_VALUES.items():
                v_match = re.search(rf"^\s+{re.escape(key)}:\s*(.+?)$", block, re.MULTILINE)
                if not v_match:
                    continue
                raw = v_match.group(1).strip().strip('"').strip("'")
                if raw.lower() in ("null", "~", ""):
                    continue
                if raw not in allowed:
                    report.warn(
                        "brief-scenarios",
                        f"{rel}: scenario.{key} value '{raw}' not in spec-fixed enum {sorted(allowed)}",
                    )


def _strip_blurb(text: str) -> str:
    """Remove the canonical Messaging System Reference blurb section from skill text.

    Strips from the `## Messaging System Reference` heading up to (but not including)
    the next H2. Lets check_duplicates ignore the canonical text that's deliberately
    shared across every conformant skill.
    """
    pattern = re.compile(
        r"^##\s+Messaging\s+System\s+Reference\s*$.*?(?=^##\s+\S)",
        re.MULTILINE | re.DOTALL,
    )
    return pattern.sub("", text)


def check_duplicates(report: Report) -> None:
    """#11 Flag shared 5+ consecutive line sequences across SKILL.md files."""
    report.begin("duplicates")
    if not SKILLS_DIR.exists():
        return
    fingerprint_to_locations: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        rel = str(skill_md.relative_to(REPO_ROOT))
        text = read_text(skill_md)
        # Strip the canonical Messaging System Reference blurb — its repetition across
        # skills is by design (single source: templates/messaging-system-reference.md).
        text = _strip_blurb(text)
        lines = text.splitlines()
        # Skip frontmatter when computing duplicates.
        if lines and lines[0].strip() == "---":
            try:
                end = lines.index("---", 1)
                lines = lines[end + 1:]
            except ValueError:
                pass
        for i in range(len(lines) - DUPLICATE_WINDOW + 1):
            window = lines[i:i + DUPLICATE_WINDOW]
            stripped = [ln.strip() for ln in window]
            # Skip windows that are mostly blank/heading runs.
            if sum(1 for s in stripped if s) < 3:
                continue
            digest = hashlib.md5("\n".join(stripped).encode("utf-8")).hexdigest()
            fingerprint_to_locations[digest].append((rel, i + 1))
    for digest, locations in fingerprint_to_locations.items():
        if len(locations) > 1 and len({loc[0] for loc in locations}) > 1:
            files = ", ".join(f"{p}:{ln}" for p, ln in locations[:4])
            more = "" if len(locations) <= 4 else f" +{len(locations) - 4} more"
            report.warn("duplicates", f"{DUPLICATE_WINDOW}+ identical lines repeated across files: {files}{more}")


def _iter_skill_and_agent_files() -> list[tuple[Path, str]]:
    """Yield (path, category) tuples for every conformance-bearing file."""
    out: list[tuple[Path, str]] = []
    if SKILLS_DIR.exists():
        for skill_md in SKILLS_DIR.rglob("SKILL.md"):
            rel_parts = skill_md.relative_to(SKILLS_DIR).parts
            category = rel_parts[0] if rel_parts else "unknown"
            out.append((skill_md, category))
    if AGENTS_DIR.exists():
        for agent_md in AGENTS_DIR.glob("*.md"):
            out.append((agent_md, "agents"))
    return out


def check_blurb_presence(report: Report) -> None:
    """#22 Warn when a skill/agent lacks the canonical Messaging System Reference blurb.

    Exempts files with `system-independent: true` in frontmatter.
    """
    report.begin("blurb-presence")
    for path, _category in _iter_skill_and_agent_files():
        text = read_text(path)
        fm = parse_frontmatter(text) or {}
        if fm.get("system-independent") is True or fm.get("system-independent") == "true":
            continue
        if BLURB_CANONICAL_PHRASE not in text:
            rel = path.relative_to(REPO_ROOT)
            report.warn(
                "blurb-presence",
                f"{rel}: missing canonical Messaging System Reference blurb (paste verbatim from `templates/messaging-system-reference.md` or mark `system-independent: true`)",
            )


def check_path_restatement(report: Report) -> None:
    """#23 Warn when skill body text restates `messaging/{pillars,collections,assets}/` paths
    as agent-facing references (i.e., not as operational paths).

    Exempts: code blocks, frontmatter, the canonical blurb section, indented (likely
    diagram) lines, and lines whose context makes the path operational — output
    destinations, template loads, removal enumerations, folder-shape descriptions,
    tool scoping, variant/slug example paths.
    """
    report.begin("path-restatement")
    exempt_markers = (
        "output", "writes to", "destination", "delete", "remove", "removal",
        "template", "tool scop", "## tool", "## modes", "## boundary",
        "folder shape", "audit log", "variants/[", "[slug]", "[variant]",
        "[name]", "[type]", "overwrite",
        "preview", "enumerate impact", "atomic deletion",
        "confirm each file",
    )
    blurb_heading_re = re.compile(r"^##\s+Messaging\s+System\s+Reference\s*$")
    h2_re = re.compile(r"^##\s+\S")
    for path, _category in _iter_skill_and_agent_files():
        text = read_text(path)
        lines = text.splitlines()
        in_frontmatter = False
        in_code_block = False
        in_blurb = False
        for i, line in enumerate(lines, start=1):
            stripped = line.lstrip()
            # Frontmatter delimiter handling (first --- opens, second --- closes).
            if i == 1 and stripped == "---":
                in_frontmatter = True
                continue
            if in_frontmatter:
                if stripped == "---":
                    in_frontmatter = False
                continue
            # Blurb section handling.
            if blurb_heading_re.match(stripped):
                in_blurb = True
                continue
            if in_blurb and h2_re.match(stripped):
                in_blurb = False
                # fall through to check this line
            if in_blurb:
                continue
            # Code block handling.
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            # Skip likely diagram / tree lines (indented 4+ chars).
            if len(line) - len(line.lstrip(" ")) >= 4:
                continue
            lower = line.lower()
            if any(marker in lower for marker in exempt_markers):
                continue
            for pat in RESTATEMENT_PATH_PATTERNS:
                if pat.search(line):
                    rel = path.relative_to(REPO_ROOT)
                    report.warn(
                        "path-restatement",
                        f"{rel}:{i}: hardcoded messaging path — consider replacing with a name-based reference (e.g., 'the position pillar')",
                    )
                    break


def _split_design_md(text: str) -> tuple[str, str] | None:
    """Split DESIGN.md into (frontmatter_block, body). Returns None if no frontmatter."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    return text[4:end], text[end + 4 :]


def _top_level_yaml_keys(frontmatter: str) -> set[str]:
    """Return the set of top-level keys in a YAML block (lines starting at column 0 with `key:`)."""
    keys: set[str] = set()
    for line in frontmatter.splitlines():
        if not line or line.startswith("#") or line.startswith(" ") or line.startswith("\t"):
            continue
        if ":" in line:
            keys.add(line.split(":", 1)[0].strip())
    return keys


def _yaml_block(frontmatter: str, key: str) -> str | None:
    """Return the indented body of a top-level YAML mapping key, or None if missing/scalar."""
    lines = frontmatter.splitlines()
    in_block = False
    out: list[str] = []
    for line in lines:
        if not in_block:
            if line.startswith(f"{key}:"):
                # Scalar value on same line means no block body
                if line[len(key) + 1 :].strip() and not line.rstrip().endswith(":"):
                    return None
                in_block = True
                continue
        else:
            if line and not line.startswith(" ") and not line.startswith("\t"):
                break
            out.append(line)
    return "\n".join(out) if in_block else None


def _subkeys(block: str) -> set[str]:
    """Return immediate child keys of a YAML block (2-space-indented `key:` lines)."""
    keys: set[str] = set()
    for line in block.splitlines():
        # Match `  key:` exactly two-space-indented
        if re.match(r"^  [a-zA-Z0-9_-]+:", line):
            keys.add(line.strip().rstrip(":").split(":", 1)[0])
    return keys


def _extract_brand_asset_paths(frontmatter: str) -> list[tuple[str, str]]:
    """From the `assets:` block, return [(token_path, file_path), ...] for every leaf string value."""
    assets_block = _yaml_block(frontmatter, "assets")
    if assets_block is None:
        return []
    results: list[tuple[str, str]] = []
    current_category: str | None = None
    for line in assets_block.splitlines():
        # Category line: "  logos:" (2-space indent, key, colon, no value)
        m = re.match(r"^  ([a-zA-Z0-9_-]+):\s*$", line)
        if m:
            current_category = m.group(1)
            continue
        # Leaf line: "    primary: \"brand/logos/primary.svg\"" (4-space indent)
        m = re.match(r'^    ([a-zA-Z0-9_-]+):\s*["\']?([^"\']+?)["\']?\s*$', line)
        if m and current_category:
            results.append((f"assets.{current_category}.{m.group(1)}", m.group(2).strip()))
    return results


def _extract_token_references(frontmatter: str) -> list[tuple[int, str]]:
    """Find every {path.to.token} reference within the components: block. Returns [(line_in_fm, token_path), ...]."""
    components_block = _yaml_block(frontmatter, "components")
    if components_block is None:
        return []
    results: list[tuple[int, str]] = []
    pattern = re.compile(r"\{([a-zA-Z0-9_.-]+)\}")
    for i, line in enumerate(components_block.splitlines(), start=1):
        for m in pattern.finditer(line):
            results.append((i, m.group(1)))
    return results


def _token_exists(frontmatter: str, dotted_path: str) -> bool:
    """Check whether `colors.primary` / `rounded.md` style reference resolves to a defined leaf."""
    parts = dotted_path.split(".")
    if not parts:
        return False
    top = parts[0]
    block = _yaml_block(frontmatter, top)
    if block is None:
        return False
    # Walk down the indentation tree.
    expected_indent = 2
    remaining = parts[1:]
    current_block = block
    while remaining:
        key = remaining[0]
        found = False
        # Look for `<key>:` at the expected indent within current_block.
        prefix = " " * expected_indent + key + ":"
        for line in current_block.splitlines():
            if line.startswith(prefix):
                found = True
                if len(remaining) == 1:
                    return True
                # Descend: collect the sub-block for further walking.
                sub_lines: list[str] = []
                started = False
                for sub in current_block.splitlines():
                    if sub.startswith(prefix):
                        started = True
                        continue
                    if started:
                        if sub and not sub.startswith(" " * (expected_indent + 2)):
                            break
                        sub_lines.append(sub)
                current_block = "\n".join(sub_lines)
                expected_indent += 2
                break
        if not found:
            return False
        remaining = remaining[1:]
    return True


def check_design_md_spec(report: Report) -> None:
    """#25 brand/DESIGN.md conforms to the Google Labs DESIGN.md spec (required frontmatter + body sections)."""
    report.begin("design-md-spec")
    if not BRAND_DESIGN_MD.exists():
        return  # Brand foundation not initialized; check no-ops.
    text = read_text(BRAND_DESIGN_MD)
    split = _split_design_md(text)
    if split is None:
        report.err("design-md-spec", "brand/DESIGN.md: missing YAML frontmatter (expected leading `---` block)")
        return
    frontmatter, body = split
    required_fm = {"version", "name", "colors", "typography"}
    present = _top_level_yaml_keys(frontmatter)
    missing_fm = required_fm - present
    if missing_fm:
        report.err(
            "design-md-spec",
            f"brand/DESIGN.md: missing required frontmatter keys: {sorted(missing_fm)}",
        )
    required_sections = ["## Overview", "## Colors", "## Typography"]
    for section in required_sections:
        if section not in body:
            report.err("design-md-spec", f"brand/DESIGN.md: missing required body section `{section}`")


def check_design_md_minimums(report: Report) -> None:
    """#26 brand/DESIGN.md defines minimum tokens (primary color, headline-lg + body-md typography, button-primary component)."""
    report.begin("design-md-minimums")
    if not BRAND_DESIGN_MD.exists():
        return
    text = read_text(BRAND_DESIGN_MD)
    split = _split_design_md(text)
    if split is None:
        return
    frontmatter, _ = split
    minimums = [
        ("colors", "primary"),
        ("typography", "headline-lg"),
        ("typography", "body-md"),
        ("components", "button-primary"),
    ]
    for top, sub in minimums:
        block = _yaml_block(frontmatter, top)
        if block is None:
            report.warn("design-md-minimums", f"brand/DESIGN.md: missing `{top}:` block — minimum {top}.{sub} undefined")
            continue
        if sub not in _subkeys(block):
            report.warn(
                "design-md-minimums",
                f"brand/DESIGN.md: missing minimum token `{top}.{sub}` — producer may fall back",
            )


def check_brand_asset_resolution(report: Report) -> None:
    """#27 Every path declared in brand/DESIGN.md's assets: block resolves to a file on disk."""
    report.begin("brand-asset-resolution")
    if not BRAND_DESIGN_MD.exists():
        return
    text = read_text(BRAND_DESIGN_MD)
    split = _split_design_md(text)
    if split is None:
        return
    frontmatter, _ = split
    for token_path, file_path in _extract_brand_asset_paths(frontmatter):
        # Resolve relative to repo root.
        resolved = REPO_ROOT / file_path
        if not resolved.exists():
            report.warn(
                "brand-asset-resolution",
                f"brand/DESIGN.md: {token_path} → `{file_path}` does not exist on disk (producer will fall back or refuse for this asset)",
            )


def check_design_token_references(report: Report) -> None:
    """#28 Every {path.to.token} reference inside components: resolves to a defined token."""
    report.begin("design-token-references")
    if not BRAND_DESIGN_MD.exists():
        return
    text = read_text(BRAND_DESIGN_MD)
    split = _split_design_md(text)
    if split is None:
        return
    frontmatter, _ = split
    for _line_no, ref in _extract_token_references(frontmatter):
        if not _token_exists(frontmatter, ref):
            report.err(
                "design-token-references",
                f"brand/DESIGN.md: unresolved token reference `{{{ref}}}` in components block",
            )


def check_asset_production_targets(report: Report) -> None:
    """#29 Asset templates' production-targets: values are valid (web/email/print or a custom produce-* skill)."""
    report.begin("asset-production-targets")
    valid_targets = set(STANDARD_PRODUCTION_TARGETS)
    # Discover custom production targets from tasks/produce-* skills.
    tasks_dir = SKILLS_DIR / "tasks"
    if tasks_dir.exists():
        for sub in tasks_dir.iterdir():
            if sub.is_dir() and sub.name.startswith("produce-"):
                valid_targets.add(sub.name[len("produce-") :])

    # Scan both populated assets and templates.
    asset_files: list[Path] = []
    if ASSETS_DIR.exists():
        asset_files.extend(ASSETS_DIR.rglob("asset.md"))
    if TEMPLATE_ASSETS_DIR.exists():
        asset_files.extend(TEMPLATE_ASSETS_DIR.rglob("asset.md"))

    for path in asset_files:
        text = read_text(path)
        split = _split_design_md(text)  # reuse the frontmatter splitter (same shape)
        if split is None:
            continue
        frontmatter, _ = split
        # Find `production-targets:` block — values are `  - <name>` lines.
        block_match = re.search(r"^production-targets:\s*(?:\[(.*?)\]|\n((?:  - .+\n?)*))",
                                 frontmatter, re.MULTILINE)
        if not block_match:
            continue
        inline, multiline = block_match.group(1), block_match.group(2)
        values: list[str] = []
        if inline is not None:
            values = [v.strip().strip('"').strip("'") for v in inline.split(",") if v.strip()]
        elif multiline:
            for ln in multiline.splitlines():
                m = re.match(r"^  - (.+)$", ln)
                if m:
                    values.append(m.group(1).strip().strip('"').strip("'"))
        rel = path.relative_to(REPO_ROOT)
        for v in values:
            if v not in valid_targets:
                report.warn(
                    "asset-production-targets",
                    f"{rel}: production-target `{v}` not in {sorted(valid_targets)} — typo or missing tasks/produce-{v}/ skill?",
                )


def check_skill_length(report: Report) -> None:
    """#24 Warn when skill files exceed length thresholds (informational only)."""
    report.begin("skill-length")
    if not SKILLS_DIR.exists():
        return
    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        rel = skill_md.relative_to(REPO_ROOT)
        rel_in_skills = skill_md.relative_to(SKILLS_DIR).parts
        category = rel_in_skills[0] if rel_in_skills else "unknown"
        threshold = SKILL_LENGTH_THRESHOLDS.get(category, 250)
        line_count = len(read_text(skill_md).splitlines())
        if line_count > threshold:
            report.warn(
                "skill-length",
                f"{rel}: {line_count} lines exceeds {threshold}-line threshold for {category} skills — audit for restatement",
            )


# ----- Helpers -----

def _scan_pattern(
    report: Report,
    check_id: str,
    pattern: re.Pattern[str],
    *,
    message_fmt: str,
    roots: list[Path],
    permissive: set[Path] = frozenset(),
) -> None:
    targets: list[Path] = []
    for root in roots:
        if root.is_file():
            targets.append(root)
        elif root.is_dir():
            targets.extend(discover_markdown(root))
    for path in targets:
        if path in permissive:
            continue
        text = read_text(path)
        for i, line in enumerate(text.splitlines(), start=1):
            if pattern.search(line):
                rel = path.relative_to(REPO_ROOT)
                report.err(check_id, message_fmt.format(path=rel, line=i))


def main() -> int:
    parser = argparse.ArgumentParser(description="claude-message v1 structural validation")
    parser.add_argument("--quiet", action="store_true", help="Only emit errors and summary")
    parser.add_argument("--no-warn", action="store_true", help="Treat warnings as errors (exit 1)")
    args = parser.parse_args()

    report = Report()
    for check in (
        check_taxonomy,
        check_no_build,
        check_no_old_pillar_names,
        check_frontmatter,
        check_anatomy,
        check_cross_references,
        check_asset_variants_warn,
        check_assets,
        check_pillar_sections,
        check_duplicates,
        check_templates,
        check_no_format_paths,
        check_no_legacy_commands,
        check_asset_default_variants,
        check_asset_variants_table,
        check_message_sections,
        check_scenarios_dimensions,
        check_glossary_discipline,
        check_claude_md_sections,
        check_brief_scenarios,
        check_blurb_presence,
        check_path_restatement,
        check_design_md_spec,
        check_design_md_minimums,
        check_brand_asset_resolution,
        check_design_token_references,
        check_asset_production_targets,
        check_skill_length,
    ):
        try:
            check(report)
        except Exception as exc:  # noqa: BLE001 — surface the bug, don't crash CI
            report.err(check.__name__, f"check raised {type(exc).__name__}: {exc}")

    return report.emit(quiet=args.quiet, treat_warnings_as_errors=args.no_warn)


if __name__ == "__main__":
    sys.exit(main())
