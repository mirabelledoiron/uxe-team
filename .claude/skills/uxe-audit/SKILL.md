---
name: uxe-audit
description: Run a full design system health audit. Scans the codebase for hardcoded values that should be tokens, missing accessibility attributes, and design-to-code drift. Produces a prioritized report.
disable-model-invocation: true
context: fork
agent: general-purpose
allowed-tools: Bash(python3 *), Read, Grep, Glob
---

# Design System Audit

Scan this codebase for design system health issues and produce a prioritized report.

## Project Context

- Root: !`pwd`
- Framework: !`node -e "try{const p=require('./package.json');const d={...p.dependencies,...p.devDependencies};['react','vue','angular','svelte'].filter(k=>d[k]).forEach(k=>console.log(k))}catch(e){console.log('unknown')}" 2>/dev/null`
- Components dir: !`ls -d src/components components lib/components 2>/dev/null | head -1 || echo "src/components"`
- Token file: !`find . -maxdepth 4 \( -name "tokens.css" -o -name "tokens.json" -o -name "design-tokens.json" -o -name "*.tokens.json" \) 2>/dev/null | grep -v node_modules | head -3`

## Step 1: Run the Audit Script

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/audit.py .
```

## Step 2: Supplement with Manual Checks

After the script runs, do the following checks manually using Grep and Read:

### Token Usage Check

Search for tokens that exist but are not being used consistently:
- Find all CSS custom property definitions in token files
- Find all places where those properties are consumed
- Flag components using raw hex/px values where a token exists

### Component Completeness Check

For each component found, verify:
- All interactive states are handled (hover, focus, disabled)
- Error and loading states exist if the component is async
- Responsive behavior is defined

### Accessibility Spot Check

Sample 3–5 components from the components directory and check:
- Correct HTML element is used (button vs div, a vs button)
- `aria-label` on icon-only buttons
- Form inputs have associated labels
- Focus styles are not removed with `outline: none` without a replacement

## Step 3: Produce the Report

Output a structured report in this format:

---

# Design System Audit Report

**Date:** [today]
**Project:** [detected project name from package.json]
**Scanned:** [file counts]

## Summary

| Category | Critical | High | Medium | Low |
|----------|----------|------|--------|-----|
| Hardcoded values | | | | |
| Accessibility | | | | |
| Missing states | | | | |
| Token misuse | | | | |
| **Total** | | | | |

**Overall DS Health Score: [X]/100**

Scoring: Start at 100. -5 per Critical, -3 per High, -1 per Medium.

---

## Critical Issues

List each issue with:
- File path and line number
- What was found
- What it should be instead
- Token name to use (if applicable)

---

## High Priority Issues

Same format.

---

## Medium Priority Issues

Same format.

---

## Low Priority / Informational

Same format.

---

## What's Working Well

Call out good patterns found. DS adoption is a culture issue — positive reinforcement matters.

---

## Recommended Next Steps

Ordered by impact:
1. [Most impactful fix]
2. ...

---

## How to Fix Hardcoded Values

Quick reference for the most common fixes found:

```css
/* Before */
color: #0066CC;
padding: 16px;
border-radius: 8px;

/* After */
color: var(--color-action-primary);
padding: var(--spacing-4);
border-radius: var(--border-radius-default);
```
