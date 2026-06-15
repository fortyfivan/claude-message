#!/usr/bin/env python3
"""
validate.py — claude-message referential-integrity validation.

Runs the deterministic referential-integrity and load-bearing contract checks
against the repository — broken references and hard contract violations that are
silent until generation time, and that a script catches more reliably than a
human or an LLM. Softer structural/sync/drift checks (pillar-section structure,
collection-table sync, glossary discipline, calibration) live in `/run health`,
which is LLM-driven and better suited to judgment calls.

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
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
MESSAGING_DIR = REPO_ROOT / "messaging"
ASSETS_DIR = MESSAGING_DIR / "assets"
TEMPLATES_DIR = REPO_ROOT / "templates"
TEMPLATE_ASSETS_DIR = TEMPLATES_DIR / "assets"
MESSAGE_MD = REPO_ROOT / "MESSAGE.md"
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"
BRAND_DIR = REPO_ROOT / "brand"
BRAND_DESIGN_MD = BRAND_DIR / "DESIGN.md"

# Standard production targets shipped with claude-message.
STANDARD_PRODUCTION_TARGETS = {"web", "email", "print"}

KEBAB_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


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

def check_frontmatter(report: Report) -> None:
    """Every SKILL.md has required frontmatter fields with valid bounds."""
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


def check_assets(report: Report) -> None:
    """Every content type in MESSAGE.md's Assets table maps to either a populated asset folder OR a template."""
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


def check_asset_default_variants(report: Report) -> None:
    """Asset frontmatter `default-variant` (when non-empty) must match an existing file in the asset's variants/ directory."""
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
    """For populated assets with variants/, asset.md must have a `## Variants` table; table rows must reference real variant files; exactly one row marked default; default-variant frontmatter must agree."""
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


def check_message_sections(report: Report) -> None:
    """MESSAGE.md contains all 8 required sections (Loading lives in CLAUDE.md; ICP lives in the People pillar)."""
    report.begin("message-sections")
    if not MESSAGE_MD.exists():
        report.err("message-sections", "MESSAGE.md does not exist at repo root")
        return
    text = read_text(MESSAGE_MD)
    required_sections = [
        "## Attributes",
        "## Facts",
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
    """MESSAGE.md Scenarios section declares exactly 5 dimensions with spec-fixed enum values present."""
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


def check_claude_md_sections(report: Report) -> None:
    """CLAUDE.md contains the operating-guide sections that own loading."""
    report.begin("claude-md-sections")
    if not CLAUDE_MD.exists():
        report.err("claude-md-sections", "CLAUDE.md does not exist at repo root")
        return
    text = read_text(CLAUDE_MD)
    required_sections = [
        "## Always-On Foundation",
        "## Progressive Loading",
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
    """brand/DESIGN.md conforms to the Google Labs DESIGN.md spec (required frontmatter + body sections)."""
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
    """brand/DESIGN.md defines minimum tokens (primary color, headline-lg + body-md typography, button-primary component)."""
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
    """Every path declared in brand/DESIGN.md's assets: block resolves to a file on disk."""
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
    """Every {path.to.token} reference inside components: resolves to a defined token."""
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
    """Asset templates' production-targets: values are valid (web/email/print or a custom produce-* skill)."""
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


def main() -> int:
    parser = argparse.ArgumentParser(description="claude-message referential-integrity validation")
    parser.add_argument("--quiet", action="store_true", help="Only emit errors and summary")
    parser.add_argument("--no-warn", action="store_true", help="Treat warnings as errors (exit 1)")
    args = parser.parse_args()

    report = Report()
    for check in (
        check_frontmatter,
        check_assets,
        check_asset_default_variants,
        check_asset_variants_table,
        check_message_sections,
        check_scenarios_dimensions,
        check_claude_md_sections,
        check_design_md_spec,
        check_design_md_minimums,
        check_brand_asset_resolution,
        check_design_token_references,
        check_asset_production_targets,
    ):
        try:
            check(report)
        except Exception as exc:  # noqa: BLE001 — surface the bug, don't crash CI
            report.err(check.__name__, f"check raised {type(exc).__name__}: {exc}")

    return report.emit(quiet=args.quiet, treat_warnings_as_errors=args.no_warn)


if __name__ == "__main__":
    sys.exit(main())
