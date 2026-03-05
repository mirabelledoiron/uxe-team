---
name: uxe-token-gen
description: Generate a complete design token system from a brand color. Outputs colors, typography, spacing, shadows, border radius, animation, breakpoints, and z-index in any format. Use when creating or updating a design system's token foundation.
argument-hint: <#hex> [modern|classic|playful] [css|scss|js|tailwind|style-dictionary|summary]
disable-model-invocation: true
allowed-tools: Bash(python3 *)
---

# Design Token Generator

Generate a complete, production-ready design token system from a single brand color.

## Usage

```bash
/uxe-token-gen #0066CC
/uxe-token-gen #0066CC modern css
/uxe-token-gen #FF6B6B playful tailwind
/uxe-token-gen #2D3748 classic style-dictionary
/uxe-token-gen #0066CC modern summary
```

## Arguments

| Argument | Options | Default | Description |
|----------|---------|---------|-------------|
| `hex` | Any 6-digit hex | Required | Brand primary color |
| `style` | `modern` `classic` `playful` | `modern` | Visual style preset |
| `format` | `css` `scss` `js` `tailwind` `style-dictionary` `summary` | `css` | Output format |

## Style Presets

| Aspect | Modern | Classic | Playful |
|--------|--------|---------|---------|
| Font | Inter | Helvetica Neue | Poppins |
| Radius | 8px | 4px | 16px |
| Shadows | Layered, subtle | Single layer | Soft, pronounced |

## What Gets Generated

- **Colors** — primary scale (50–950), secondary (complementary hue), neutral (brand-tinted grays), semantic (success/warning/error/info), surface, text, border
- **Typography** — font families, size scale (xs–5xl, 1.25x ratio), weights, line heights, letter spacing
- **Spacing** — 4pt/8pt grid (0–128px)
- **Border radius** — none through full, per style preset
- **Shadows** — xs through 2xl + inner
- **Animation** — duration tokens (50ms–500ms), easing curves
- **Breakpoints** — xs through 3xl (480px steps)
- **Z-index** — semantic scale (base through max)

## Run

Run the bundled script with your arguments:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/token_gen.py $ARGUMENTS
```

## Output Examples

### CSS
```css
:root {
  --color-primary-500: #0066CC;
  --color-primary-600: #0057AD;
  --spacing-4: 16px;
  --font-size-base: 1rem;
}
```

### Tailwind
```js
module.exports = {
  theme: {
    extend: {
      colors: { primary: { 500: '#0066CC', ... } }
    }
  }
}
```

### Style Dictionary
Outputs W3C Design Tokens Community Group format — compatible with Tokens Studio, Style Dictionary 4+, and theo.

## After Generation

1. Review the `summary` format first to check colors and contrast ratios
2. Check WCAG contrast on primary-500 — the script reports this
3. Export in your project's format
4. For Figma sync: use `style-dictionary` format with Tokens Studio plugin
5. Commit tokens as the single source of truth
