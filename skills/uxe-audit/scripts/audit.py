#!/usr/bin/env python3
"""
uxe-audit — Design system health scanner.
Part of the uxe-team Claude agent toolkit.

Usage:
    python3 audit.py [directory]

    directory : Root of codebase to scan (default: current directory)

Scans for:
  - Hardcoded color values that should be design tokens
  - Hardcoded spacing/sizing values that should be tokens
  - Interactive elements missing accessibility attributes
  - Inline styles (design system anti-pattern)
  - Components with 'onClick' but missing keyboard handlers
"""

import sys
import os
import re
import json
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Tuple


# ── Patterns ───────────────────────────────────────────────────────────────────

# Colors: hex, rgb(), rgba(), hsl(), hsla()
COLOR_PATTERNS = [
    (re.compile(r'#(?:[0-9a-fA-F]{3}){1,2}\b'), 'hex color'),
    (re.compile(r'rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)'), 'rgb()'),
    (re.compile(r'rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)'), 'rgba()'),
    (re.compile(r'hsl\(\s*\d+\s*,\s*\d+%\s*,\s*\d+%\s*\)'), 'hsl()'),
]

# Spacing: bare px values in style/className context (not in border-radius, etc.)
# We look for patterns like: padding: 16px, margin: 8px 16px, gap: 24px
SPACING_PATTERN = re.compile(
    r'(?:padding|margin|gap|top|right|bottom|left|width|height|min-width|max-width|min-height|max-height|font-size|line-height)\s*:\s*([\d.]+px)',
)

# Inline style attributes in JSX/HTML
INLINE_STYLE_PATTERN = re.compile(r'\bstyle\s*=\s*\{?\s*[{"\'`]')

# onClick without onKeyDown/onKeyPress (potential keyboard accessibility gap)
ONCLICK_PATTERN = re.compile(r'\bonClick\b')
ONKEY_PATTERN   = re.compile(r'\bon(?:KeyDown|KeyPress|KeyUp)\b')

# aria-label missing on icon-only buttons (rough heuristic)
ICON_BUTTON_PATTERN = re.compile(r'<(?:button|Button)[^>]*>\s*<(?:Icon|Svg|svg|img)[^/]*/>\s*</(?:button|Button)>')

# outline: none / outline: 0 without focus-visible replacement
OUTLINE_NONE_PATTERN = re.compile(r'outline\s*:\s*(?:none|0)\b')
FOCUS_VISIBLE_PATTERN = re.compile(r':focus-visible')

# CSS var usage (correct pattern)
CSS_VAR_PATTERN = re.compile(r'var\(--[\w-]+\)')

# Tailwind classes that look like hardcoded colors (e.g. text-[#0066CC])
TAILWIND_ARBITRARY_COLOR = re.compile(r'(?:text|bg|border|fill|stroke)-\[#[0-9a-fA-F]{3,6}\]')


# ── File Discovery ─────────────────────────────────────────────────────────────

SKIP_DIRS = {
    'node_modules', '.git', 'dist', 'build', '.next', '.nuxt',
    'coverage', '__pycache__', '.cache', 'storybook-static',
}

SOURCE_EXTENSIONS = {'.css', '.scss', '.sass', '.less', '.tsx', '.ts', '.jsx', '.js', '.vue', '.svelte', '.html'}
STYLE_EXTENSIONS  = {'.css', '.scss', '.sass', '.less'}
COMPONENT_EXTENSIONS = {'.tsx', '.jsx', '.vue', '.svelte'}


def find_files(root: Path) -> List[Path]:
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            p = Path(dirpath) / fname
            if p.suffix in SOURCE_EXTENSIONS:
                files.append(p)
    return files


# ── Finding ────────────────────────────────────────────────────────────────────

class Finding:
    def __init__(self, severity: str, category: str, file: Path, line: int, message: str, suggestion: str = ''):
        self.severity   = severity   # CRITICAL | HIGH | MEDIUM | LOW
        self.category   = category
        self.file       = file
        self.line       = line
        self.message    = message
        self.suggestion = suggestion

    def __repr__(self):
        return f'[{self.severity}] {self.file}:{self.line} — {self.message}'


# ── Checks ─────────────────────────────────────────────────────────────────────

def check_hardcoded_colors(path: Path, lines: List[str]) -> List[Finding]:
    findings = []
    # Skip token definition files themselves
    if path.name in ('tokens.css', 'design-tokens.json', 'tokens.json') or 'tokens' in path.parts:
        return findings
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('*') or stripped.startswith('#'):
            continue
        for pattern, label in COLOR_PATTERNS:
            for match in pattern.finditer(line):
                value = match.group(0)
                # Allow common non-token cases: transparent, white, black in shadows
                if value.lower() in ('#fff', '#ffffff', '#000', '#000000'):
                    continue
                if 'box-shadow' in line.lower() and 'rgb(0 0 0' in line.lower():
                    continue
                findings.append(Finding(
                    severity='HIGH',
                    category='hardcoded-color',
                    file=path, line=i,
                    message=f'Hardcoded {label}: {value}',
                    suggestion='Replace with a CSS custom property: var(--color-...)',
                ))
    return findings


def check_hardcoded_spacing(path: Path, lines: List[str]) -> List[Finding]:
    findings = []
    if path.suffix not in STYLE_EXTENSIONS:
        return findings
    if path.name in ('tokens.css', 'design-tokens.css') or 'tokens' in path.parts:
        return findings
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('*') or stripped.startswith('--'):
            continue
        for match in SPACING_PATTERN.finditer(line):
            value = match.group(1)
            px_val = float(value.replace('px', ''))
            # Only flag values that should obviously be tokens (multiples of 4)
            if px_val % 4 == 0 and px_val > 0:
                findings.append(Finding(
                    severity='MEDIUM',
                    category='hardcoded-spacing',
                    file=path, line=i,
                    message=f'Hardcoded spacing: {value}',
                    suggestion=f'Use spacing token: var(--spacing-{int(px_val // 4)})',
                ))
    return findings


def check_inline_styles(path: Path, lines: List[str]) -> List[Finding]:
    findings = []
    if path.suffix not in COMPONENT_EXTENSIONS:
        return findings
    for i, line in enumerate(lines, 1):
        if INLINE_STYLE_PATTERN.search(line):
            # Skip Storybook args, test fixtures, and token-injecting patterns
            if any(skip in line for skip in ['args=', 'story', 'test', 'mock', 'CSSProperties']):
                continue
            findings.append(Finding(
                severity='MEDIUM',
                category='inline-style',
                file=path, line=i,
                message='Inline style attribute found',
                suggestion='Move styles to CSS/Tailwind using design tokens',
            ))
    return findings


def check_click_without_keyboard(path: Path, lines: List[str]) -> List[Finding]:
    findings = []
    if path.suffix not in COMPONENT_EXTENSIONS:
        return findings
    full_text = '\n'.join(lines)
    # Get line numbers of all onClick occurrences
    for i, line in enumerate(lines, 1):
        if ONCLICK_PATTERN.search(line):
            # Check surrounding context (±5 lines) for keyboard handler
            context_start = max(0, i - 6)
            context_end   = min(len(lines), i + 5)
            context = '\n'.join(lines[context_start:context_end])
            if not ONKEY_PATTERN.search(context):
                # Check if it's on a native button/a (which has keyboard built-in)
                if not re.search(r'<(?:button|a|input|select|textarea)\b', context, re.I):
                    findings.append(Finding(
                        severity='HIGH',
                        category='accessibility',
                        file=path, line=i,
                        message='onClick without keyboard handler on non-native element',
                        suggestion='Add onKeyDown handler or use <button> instead of div/span',
                    ))
    return findings


def check_outline_none(path: Path, lines: List[str]) -> List[Finding]:
    findings = []
    if path.suffix not in STYLE_EXTENSIONS and path.suffix not in COMPONENT_EXTENSIONS:
        return findings
    full_text = '\n'.join(lines)
    if OUTLINE_NONE_PATTERN.search(full_text) and not FOCUS_VISIBLE_PATTERN.search(full_text):
        # Find the line
        for i, line in enumerate(lines, 1):
            if OUTLINE_NONE_PATTERN.search(line):
                findings.append(Finding(
                    severity='CRITICAL',
                    category='accessibility',
                    file=path, line=i,
                    message='outline: none/0 without :focus-visible replacement',
                    suggestion='Add a visible :focus-visible style. Never remove focus indicators.',
                ))
    return findings


def check_tailwind_arbitrary_colors(path: Path, lines: List[str]) -> List[Finding]:
    findings = []
    for i, line in enumerate(lines, 1):
        for match in TAILWIND_ARBITRARY_COLOR.finditer(line):
            findings.append(Finding(
                severity='HIGH',
                category='hardcoded-color',
                file=path, line=i,
                message=f'Tailwind arbitrary color: {match.group(0)}',
                suggestion='Use a Tailwind color token instead: bg-primary-500',
            ))
    return findings


# ── Scoring ────────────────────────────────────────────────────────────────────

SEVERITY_SCORE = {'CRITICAL': 5, 'HIGH': 3, 'MEDIUM': 1, 'LOW': 0}

def health_score(findings: List[Finding]) -> int:
    deduction = sum(SEVERITY_SCORE.get(f.severity, 0) for f in findings)
    return max(0, 100 - deduction)


# ── Report ─────────────────────────────────────────────────────────────────────

def group_by_severity(findings: List[Finding]) -> Dict[str, List[Finding]]:
    groups = defaultdict(list)
    for f in findings:
        groups[f.severity].append(f)
    return groups


def print_report(findings: List[Finding], root: Path, file_count: int):
    groups     = group_by_severity(findings)
    score      = health_score(findings)
    cat_counts = defaultdict(lambda: defaultdict(int))
    for f in findings:
        cat_counts[f.category][f.severity] += 1

    print(f'\n{"="*60}')
    print(f'  uxe-audit — Design System Health Report')
    print(f'{"="*60}')
    print(f'  Root     : {root}')
    print(f'  Files    : {file_count} source files scanned')
    print(f'  Issues   : {len(findings)} total')
    print(f'  Score    : {score}/100')
    print(f'{"="*60}\n')

    # Summary table
    categories = sorted(cat_counts.keys())
    print(f'{"Category":<25} {"CRITICAL":>8} {"HIGH":>6} {"MEDIUM":>7} {"LOW":>5}')
    print('-' * 55)
    for cat in categories:
        c = cat_counts[cat]
        print(f'  {cat:<23} {c.get("CRITICAL",0):>8} {c.get("HIGH",0):>6} {c.get("MEDIUM",0):>7} {c.get("LOW",0):>5}')
    print()

    for severity in ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW'):
        items = groups.get(severity, [])
        if not items:
            continue
        print(f'\n── {severity} ({len(items)}) {"─" * (50 - len(severity))}')
        for f in items:
            rel = f.file.relative_to(root) if f.file.is_relative_to(root) else f.file
            print(f'  {rel}:{f.line}')
            print(f'    {f.message}')
            if f.suggestion:
                print(f'    → {f.suggestion}')

    print(f'\n{"="*60}')
    print(f'  Overall health: {score}/100', end='  ')
    if score >= 90:
        print('Excellent')
    elif score >= 75:
        print('Good')
    elif score >= 60:
        print('Needs attention')
    else:
        print('Significant work needed')
    print(f'{"="*60}\n')


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    if not root.is_dir():
        print(f'Error: "{root}" is not a directory', file=sys.stderr)
        sys.exit(1)

    files = find_files(root)
    all_findings: List[Finding] = []

    for path in files:
        try:
            text  = path.read_text(encoding='utf-8', errors='ignore')
            lines = text.splitlines()
        except Exception:
            continue

        all_findings.extend(check_hardcoded_colors(path, lines))
        all_findings.extend(check_hardcoded_spacing(path, lines))
        all_findings.extend(check_inline_styles(path, lines))
        all_findings.extend(check_click_without_keyboard(path, lines))
        all_findings.extend(check_outline_none(path, lines))
        all_findings.extend(check_tailwind_arbitrary_colors(path, lines))

    # Sort: critical first, then by file
    severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    all_findings.sort(key=lambda f: (severity_order.get(f.severity, 4), str(f.file), f.line))

    print_report(all_findings, root, len(files))

    # Exit code: 0 = clean, 1 = has critical/high, 2 = has medium/low only
    criticals = [f for f in all_findings if f.severity in ('CRITICAL', 'HIGH')]
    sys.exit(1 if criticals else (2 if all_findings else 0))


if __name__ == '__main__':
    main()
