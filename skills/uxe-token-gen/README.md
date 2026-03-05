# uxe-token-gen

Generate a complete design token set from a single brand color.

## Usage

```
/uxe-token-gen #0066CC modern css
/uxe-token-gen #e94560 playful tailwind
/uxe-token-gen #22c55e classic scss
/uxe-token-gen #3b82f6 modern style-dictionary
/uxe-token-gen #f59e0b modern summary
```

**Syntax:** `/uxe-token-gen <#hex> [modern|classic|playful] [css|scss|js|tailwind|style-dictionary|summary]`

Both arguments are optional. Defaults: `modern`, `css`.

## What it generates

From one hex color:

- **Color scale** (50–950) — 11 shades from near-white to near-black
- **Neutral scale** — desaturated gray scale
- **Secondary scale** — complementary hue color scale
- **Semantic tokens** — background, foreground, primary, secondary, muted, border, ring, destructive, success, warning, info
- **Typography** — font families, size scale (xs through 5xl), weights, line heights
- **Spacing** — 8pt grid from 1 to 96
- **Border radius** — none, sm, default, md, lg, xl, full
- **Shadows** — sm, default, md, lg, xl
- **Motion** — duration (fast, base, slow, slower) and easing tokens
- **Breakpoints** — sm, md, lg, xl, 2xl
- **Z-index** — semantic scale (dropdown, sticky, fixed, overlay, modal, tooltip)

## Output formats

| Format | Output |
|--------|--------|
| `css` | CSS custom properties (`:root { --color-primary-500: ... }`) |
| `scss` | SCSS variables (`$color-primary-500: ...`) |
| `js` | ES module export (`export const tokens = { ... }`) |
| `tailwind` | Tailwind config object (`module.exports = { theme: { ... } }`) |
| `style-dictionary` | W3C DTCG format JSON |
| `summary` | Human-readable overview of all generated values |

## Installation

```bash
cp -r skills/uxe-token-gen ~/.claude/skills/
```

Python 3 required. No external dependencies.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill file with YAML frontmatter |
| `scripts/token_gen.py` | Token generation engine — no external dependencies |
| `README.md` | This file |
