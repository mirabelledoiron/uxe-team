# uxe-context

Always-on UXE background knowledge. Automatically loaded by Claude when you're working in a project that has this skill installed. No slash command needed.

## What it does

Puts Claude in UX Engineering mode. It knows:
- The three pillars of a design system (Design Language, Component Library, Style Guide)
- Token hierarchy: primitive → semantic → component
- Accessibility fundamentals (ARIA, keyboard patterns, WCAG criteria)
- Component state checklist (default, hover, focus, active, disabled, loading, error, empty)
- The designer-engineer translation map
- Visual design reasoning (why we left-align, why 50-70 char line lengths, why dark-on-light)

It also auto-detects your live project stack using shell injection — framework, TypeScript, Storybook, token files, components directory.

## Installation

```bash
cp -r skills/uxe-context ~/.claude/skills/
```

## Customizing for your design system

Edit `SKILL.md` to add your actual token names, component inventory, and conventions. The more specific you make it, the more useful Claude becomes.

For a fully personalized example, see the `atelier-uxe-team` repo.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill file with YAML frontmatter and content |
| `design-principles.md` | Full UXE knowledge base — loaded as reference material |
| `README.md` | This file |
