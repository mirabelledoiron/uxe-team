# uxe-team — WIP

A virtual UX Engineering team for Claude Code. Drop it into any project and get UXE capabilities embedded in your workflow — regardless of framework or token format.

---

## What Is This?

A UX Engineer (UXE) sits between design and engineering. They translate design intent into technical spec, maintain design systems, and close the gap that causes most design-to-code drift.

This project gives any team that gap-closing capability through Claude skills and agents:

- **Skills** — background knowledge Claude applies automatically, plus commands you invoke directly
- **Agents** — specialists you call on for deep, focused work

---

## What's Included

### Skills

| Skill | How invoked | What it does |
|-------|-------------|--------------|
| `uxe-context` | Automatic | Always-on UXE background knowledge. Auto-detects your stack. |
| `uxe-token-gen` | `/uxe-token-gen` | Generate a complete token set from a brand color, in any format |
| `uxe-scaffold` | `/uxe-scaffold` | Scaffold a component for any framework |
| `uxe-audit` | `/uxe-audit` | Full DS health check — hardcoded values, token misuse, a11y gaps |

### Agents

| Agent | What it does |
|-------|--------------|
| `uxe-bridge` | Translates design specs into engineering specs. The core of this team. |
| `uxe-token-architect` | Token naming, hierarchy, multi-format output. Remembers your DS decisions. |
| `uxe-a11y` | WCAG, ARIA, focus management, semantic markup — design and code sides |
| `uxe-component-writer` | Generates style guide documentation for both designers and developers |
| `uxe-reviewer` | Validates that code matches design intent |

---

## Installation

### For a specific project

```bash
cp -r .claude /your/project/.claude
```

### For all your projects (personal)

```bash
cp -r .claude/skills/* ~/.claude/skills/
cp -r .claude/agents/* ~/.claude/agents/
```

### Selective install

```bash
# Just the background context + bridge agent (recommended starting point)
cp -r .claude/skills/uxe-context ~/.claude/skills/
cp .claude/agents/uxe-bridge.md ~/.claude/agents/
```

---

## Usage

### The most common workflow

A designer hands off a component. Instead of a long back-and-forth, use the bridge agent:

```
Use uxe-bridge to spec out the Card component from this design:
- White background, 16px padding, brand shadow
- Header slot, body text, optional CTA button
- Used in dashboard and listing pages
```

The agent returns a full technical spec: props, variants, states, tokens, accessibility requirements, responsive behavior, and a list of questions for the designer.

### Token generation

```
/uxe-token-gen #0066CC modern css
```

Outputs a complete token set (colors, typography, spacing, shadows, breakpoints) in CSS custom properties, SCSS, JavaScript, or Style Dictionary format.

### Full DS audit

```
/uxe-audit
```

Scans the codebase for hardcoded values that should be tokens, components missing accessibility attributes, and design-code drift.

---

## Design Philosophy

This project is built around three ideas:

1. **The UXE is the bridge** — the biggest DS problems are translation problems, not technical ones
2. **Stack-agnostic** — works with React, Vue, Angular, Svelte, Web Components, any token format
3. **Knowledge compounds** — agents with `memory: project` build institutional knowledge about your DS over time

---

## The Three Pillars of a Design System

This team covers all three:

| Pillar | What it is | Covered by |
|--------|-----------|------------|
| Design Language | Color, typography, spacing, animation, brand | `uxe-token-gen`, `uxe-token-architect` |
| Component Library | Coded components for all frameworks | `uxe-scaffold`, `uxe-bridge`, `uxe-reviewer` |
| Style Guide | Documentation website | `uxe-component-writer` |

---

## Status

| File | Status |
|------|--------|
| `uxe-context` skill | Done |
| `uxe-bridge` agent | Done |
| `uxe-token-gen` skill | Coming |
| `uxe-scaffold` skill | Coming |
| `uxe-audit` skill | Coming |
| `uxe-token-architect` agent | Coming |
| `uxe-a11y` agent | Coming |
| `uxe-component-writer` agent | Coming |
| `uxe-reviewer` agent | Coming |

---

## Contributing

Built to be open and extended. Each skill and agent is a standalone file — add your own, customize the prompts, share back what works.

---

MIT License
