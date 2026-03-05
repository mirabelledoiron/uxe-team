# CLAUDE.md — uxe-team

This repository is a UX Engineering agent team for Claude Code. It provides skills and agents that close the designer-to-engineer gap on any design system team.

**This is not a development project.** It is a library of skills and agents you install into your own projects. Focus on helping users install, understand, customize, and extend these files for their own design systems.

---

## Repository Purpose

UX Engineers sit between design and engineering. They translate design intent into technical spec, maintain design systems, and prevent the drift that causes most design-to-code failures.

This library gives any team that capability through Claude — without manual context-setting every session.

---

## Structure

```
uxe-team/
├── CLAUDE.md                        # This file — always loaded by Claude
├── README.md                        # Project overview and usage guide
├── skills/                          # Source skills — install to ~/.claude/skills/
│   ├── uxe-context/                 # Always-on background knowledge
│   │   ├── SKILL.md
│   │   ├── design-principles.md
│   │   └── README.md
│   ├── uxe-token-gen/               # Token generator from brand color
│   │   ├── SKILL.md
│   │   ├── scripts/token_gen.py
│   │   └── README.md
│   ├── uxe-scaffold/                # Component scaffolder
│   │   ├── SKILL.md
│   │   └── README.md
│   └── uxe-audit/                   # DS health check scanner
│       ├── SKILL.md
│       ├── scripts/audit.py
│       └── README.md
├── agents/                          # Source agents — install to ~/.claude/agents/
│   ├── uxe-bridge.md                # Design-to-engineering translator (core)
│   ├── uxe-token-architect.md       # Token structure specialist
│   ├── uxe-a11y.md                  # WCAG 2.1 AA/AAA specialist
│   ├── uxe-component-writer.md      # Style guide documentation writer
│   └── uxe-reviewer.md             # Quality gate reviewer
└── scripts/
    └── install.sh                   # Install everything to ~/.claude/
```

---

## Installation

```bash
# Install everything (recommended)
./scripts/install.sh

# Install to a specific project instead of globally
./scripts/install.sh --project /path/to/your/project

# Install only skills
./scripts/install.sh --skills

# Install only agents
./scripts/install.sh --agents
```

---

## Skills

| Skill | Invocation | What it does |
|-------|-----------|--------------|
| `uxe-context` | Automatic | Always-on UXE background knowledge. Auto-detects your stack. |
| `uxe-token-gen` | `/uxe-token-gen` | Generate a complete token set from a brand color |
| `uxe-scaffold` | `/uxe-scaffold` | Scaffold a component for any framework |
| `uxe-audit` | `/uxe-audit` | DS health check — hardcoded values, token misuse, a11y gaps |

---

## Agents

| Agent | Color | What it does |
|-------|-------|--------------|
| `uxe-bridge` | #E94560 | Translates design specs into Component Technical Specs |
| `uxe-token-architect` | #4ECDC4 | Token naming, hierarchy, multi-format output |
| `uxe-a11y` | #22C55E | WCAG 2.1 AA/AAA auditor — design and code sides |
| `uxe-component-writer` | #3B82F6 | Style guide documentation for designers and engineers |
| `uxe-reviewer` | #F59E0B | Quality gate before a component ships |

---

## Key Principles

1. **The UXE is the bridge** — the biggest DS problems are translation problems, not technical ones
2. **Stack-agnostic** — works with React, Vue, Angular, Svelte, Web Components, any token format
3. **Knowledge compounds** — agents with `memory: project` build institutional knowledge over time
4. **Don't overengineer** — keep skills as simple as possible while solving the problem
5. **Edit existing files** — prefer modifying skills over creating new ones

---

## Customizing for Your Design System

The `uxe-context` skill and `uxe-bridge` agent are the two files most worth personalizing:

- **`uxe-context/SKILL.md`** — add your actual token names, component inventory, and stack details
- **`uxe-bridge.md`** — add your component API conventions and variant patterns

See `atelier-uxe-team` for an example of a fully personalized version.
