# uxe-audit

Full design system health check. Scans your codebase for token violations and accessibility gaps, then produces a scored report.

## Usage

```
/uxe-audit
```

Run from your project root. No arguments needed.

## What it finds

| Category | What it scans for |
|----------|------------------|
| Hardcoded colors | Hex values (`#fff`, `#0066CC`), `rgb()`, `hsl()` outside token files |
| Hardcoded spacing | `px` values that should use spacing tokens |
| Inline styles | `style=` attributes in JSX/HTML |
| Missing keyboard handlers | `onClick` without `onKeyDown` or `onKeyPress` |
| Removed focus indicators | `outline: none` without `:focus-visible` replacement |
| Tailwind arbitrary values | `bg-[#0066CC]`, `p-[13px]` — should use token-based classes |

## Report format

```
DS Audit Report
Score: 74/100

CRITICAL (2)
  src/components/Button.tsx:14 — Hardcoded color: #0066CC
  src/components/Card.tsx:8 — outline: none without :focus-visible

HIGH (1)
  src/pages/Home.tsx:43 — onClick without keyboard handler

MEDIUM (3)
  ...

SUMMARY
  Files scanned: 47
  Issues found: 6
  Recommended: Fix CRITICAL and HIGH before next release
```

**Exit codes:** 0 = clean, 1 = critical/high issues found, 2 = medium/low only

## Installation

```bash
cp -r skills/uxe-audit ~/.claude/skills/
```

Python 3 required. No external dependencies.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill file — runs in forked subagent |
| `scripts/audit.py` | Static scanner — no external dependencies |
| `README.md` | This file |
